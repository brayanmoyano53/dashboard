from unidecode import unidecode # Para normalizar texto eliminando acentos y caracteres especiales
import pandas as pd  # Biblioteca principal para manipulación de datos en DataFrames
import calendar  # Para obtener nombres de meses y funciones relacionadas con fechas

# Normaliza una columna convirtiendo sus valores a texto, sin espacios y en mayúsculas.
def normalizar_codigo_columna(df, columna):
    df[columna] = df[columna].astype(str).str.strip().str.upper()
    return df

#Renombra columnas para los códigos y descripciones estandarizados.
def renombrar_columnas_codigos(df_codigos):
    return df_codigos.rename(columns={
        'Codigo de la CIE-10 cuatro caracteres': 'COD_MUERTE',
        'Descripcion  de codigos mortalidad a cuatro caracteres': 'DESCRIPCION'
    })

#Filtra filas donde la longitud del código en la columna sea mayor o igual a min_len.
def filtrar_codigos_min_length(df, columna, min_len=4):
    return df[df[columna].str.len() >= min_len]

#Filtra filas por año
def filtrar_año(df, año):
    return df[df['AÑO'] == año].copy()

# Agrupa y cuenta el total de muertes por departamento, normalizando el código departamental.
def agrupar_muertes_por_departamento(df):
    muertes = (
        df
        .groupby('COD_DEPARTAMENTO')
        .size()
        .reset_index(name='TotalMuertes')
    )
    muertes['COD_DEPARTAMENTO'] = muertes['COD_DEPARTAMENTO'].astype(int).astype(str).str.zfill(2)
    return muertes

# Obtiene una lista única de departamentos usando el nombre más frecuente por código departamental.
def obtener_departamentos_mas_frecuentes(df_division):
    frecuencias = (
        df_division
        .groupby(['COD_DEPARTAMENTO', 'DEPARTAMENTO'])
        .size()
        .reset_index(name='Frecuencia')
        .sort_values(['COD_DEPARTAMENTO', 'Frecuencia'], ascending=[True, False])
    )
    vista = (
        frecuencias
        .drop_duplicates(subset='COD_DEPARTAMENTO', keep='first')
        .drop(columns='Frecuencia')
        .sort_values('COD_DEPARTAMENTO')
    )
    vista['DEPARTAMENTO'] = vista['DEPARTAMENTO'].apply(unidecode).str.upper()
    vista['COD_DEPARTAMENTO'] = vista['COD_DEPARTAMENTO'].astype(int).astype(str).str.zfill(2)
    return vista

# Une los datos de muertes con los nombres de departamentos usando el código departamental.
def merge_muertes_departamentos(muertes, departamentos):
    return muertes.merge(departamentos, on='COD_DEPARTAMENTO', how='left')[['COD_DEPARTAMENTO', 'DEPARTAMENTO', 'TotalMuertes']]

# Agrupa y cuenta las muertes por mes, asegurando que todos los meses del año estén representados.
def agrupar_muertes_por_mes(muertes):
    muertes = muertes.copy()
    muertes['MES'] = pd.to_numeric(muertes['MES'], errors='coerce')
    
    meses = pd.Index(range(1, 13), name='MES')
    muertes_mensuales = (
        muertes.groupby('MES')
               .size()
               .reindex(meses, fill_value=0)
               .reset_index(name='TOTAL_MUERTES')
    )
    muertes_mensuales['MES_NOMBRE'] = muertes_mensuales['MES'].apply(
        lambda x: unidecode(calendar.month_name[x]).upper()
    )
    return muertes_mensuales

# Retorna las ciudades con mayor cantidad de homicidios, filtrando por un código específico de causa de muerte.
def ciudades_mas_violentas(df_muertes, df_division, top_n=5):
    df_filtrado = df_muertes[df_muertes['COD_MUERTE'].astype(str).str.lower().str.startswith('x95')]
    df_unido = df_filtrado.merge(df_division[['COD_DANE', 'MUNICIPIO']], on='COD_DANE', how='left')
    homicidios_ciudades_mas = (
        df_unido
        .groupby('MUNICIPIO')
        .size()
        .reset_index(name='TOTAL_HOMICIDIOS')
        .sort_values('TOTAL_HOMICIDIOS', ascending=False)
        .head(top_n)
    )
    return homicidios_ciudades_mas

# Retorna las ciudades con menor cantidad de muertes, basándose en los registros disponibles.
def ciudades_menos_mortalidad(df_muertes, df_division, top_n=10):
    df_unido = df_muertes.merge(df_division[['COD_DANE', 'MUNICIPIO']], on='COD_DANE', how='left')
    homicidios_ciudades_menos = (
        df_unido
        .groupby('MUNICIPIO')
        .size()
        .reset_index(name='TOTAL_HOMICIDIOS')
        .sort_values('TOTAL_HOMICIDIOS', ascending=True)
        .head(top_n)
    )
    return homicidios_ciudades_menos

# Retorna las principales causas de muerte según su frecuencia, uniendo con su descripción y mostrando las más comunes.
def causas_principales_muerte(df_muertes, df_codigos, top_n=10):
    # Normalizar código en df_muertes
    df_muertes = normalizar_codigo_columna(df_muertes, 'COD_MUERTE')
    df_muertes = filtrar_codigos_min_length(df_muertes, 'COD_MUERTE', 4)

    # Preparar df_codigos
    df_codigos = renombrar_columnas_codigos(df_codigos)
    df_codigos = normalizar_codigo_columna(df_codigos, 'COD_MUERTE')

    conteo = (
        df_muertes
        .groupby('COD_MUERTE')
        .size()
        .reset_index(name='TOTAL_CASOS')
    )

    resultado = conteo.merge(df_codigos[['COD_MUERTE', 'DESCRIPCION']], on='COD_MUERTE', how='left')
    resultado = resultado[['COD_MUERTE', 'DESCRIPCION', 'TOTAL_CASOS']]
    resultado = resultado.sort_values('TOTAL_CASOS', ascending=False).head(top_n)
    resultado['RANK'] = range(1, len(resultado) + 1)

    return resultado
# Agrupa las muertes por rangos quinquenales de edad
def conteo_muertes_por_rango_edad(df, columna='GRUPO_EDAD1'):
    # Convertir a numérico
    df[columna] = pd.to_numeric(df[columna], errors='coerce')
    df = df.dropna(subset=[columna])

    # Función para asignar rangos quinquenales
    def asignar_rango_edad(edad):
        if edad >= 85:
            return '85+'
        else:
            inicio = (edad // 5) * 5
            fin = inicio + 4
            return f'{int(inicio)}-{int(fin)}'

    df['RANGO_EDAD'] = df[columna].apply(asignar_rango_edad)

    conteo = df.groupby('RANGO_EDAD').size().reset_index(name='TOTAL_MUERTES')

    # Ordenar rangos correctamente
    def ordenar_rangos(rango):
        if rango == '85+':
            return 999
        return int(rango.split('-')[0])
    
    conteo['ORDEN'] = conteo['RANGO_EDAD'].apply(ordenar_rangos)
    conteo = conteo.sort_values('ORDEN').drop(columns='ORDEN')

    return conteo

# Agrupa las muertes por departamento y sexo, asigna nombres legibles a los sexos y añade el nombre del departamento.
def conteo_muertes_por_departamento_y_sexo(df_muertes, df_division, depto_col='COD_DEPARTAMENTO', sexo_col='SEXO', nombre_col='DEPARTAMENTO'):
    df_filtered = df_muertes[[depto_col, sexo_col]].dropna()
    df_filtered[depto_col] = df_filtered[depto_col].astype(str).str.zfill(2)
    df_division[depto_col] = df_division[depto_col].astype(str).str.zfill(2)
    conteo = (
        df_filtered
        .groupby([depto_col, sexo_col])
        .size()
        .reset_index(name='TOTAL_MUERTES')
    )

    conteo = conteo.merge(
        df_division[[depto_col, nombre_col]].drop_duplicates(),
        on=depto_col,
        how='left'
    )

    # Mapear valores de sexo a nombres
    mapa_sexo = {1: 'Masculino', 2: 'Femenino', 3: 'Otro'}
    conteo[sexo_col] = conteo[sexo_col].map(mapa_sexo).fillna('Desconocido')

    resultado = conteo[[nombre_col, sexo_col, 'TOTAL_MUERTES']]

    return resultado