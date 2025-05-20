import plotly.graph_objs as go # Importa objetos gráficos para crear gráficos personalizados
import plotly.express as px # Importa la interfaz simple para crear gráficos rápidos y fáciles

# Crear mapa con el archivo geojson
def crear_mapa(counties_geojson, locs, valores, textos):
     # Asignar el id de cada feature en el GeoJSON al código del departamento
    for loc in counties_geojson['features']:
        loc['id'] = loc['properties']['DPTO']

    # Definiendo la escala de colores
    escala_personalizada = [
        [0, "#c6e2ff"],    
        [0.25, "#91c9ff"],
        [0.5, "#5ab0ff"],
        [0.75, "#2498ff"],
        [1, "#118dff"]     
    ]

    # Crear el mapa coroplético con Plotly usando Mapbox
    fig_mapa = go.Figure(go.Choroplethmapbox(
        geojson=counties_geojson, # geometría de los departamentos
        locations=locs, # códigos de departamentos para ubicar los datos
        z=valores,   # valores numéricos para colorear (ej. total muertes)
        colorscale=escala_personalizada, # escala de colores definida arriba
        colorbar_title="Total Muertes", # título de la barra de colores
        text=textos,  # texto para mostrar al pasar el cursor
        hovertemplate='<b>%{text}</b><br>Total muertes: %{z}<extra></extra>' # formato del tooltip
    ))

    # Configurar estilo y posición del mapa
    fig_mapa.update_layout(
        mapbox_style="carto-positron", # estilo visual del mapa base
        mapbox_zoom=3.4,  # nivel de zoom inicial
        mapbox_center={"lat": 4.570868, "lon": -74.2973328},  # centro del mapa (Colombia)
        margin=dict(l=20, r=20, t=20, b=20) # márgenes alrededor del gráfico
    )
    return fig_mapa

# Crear grafico de lineas
def grafico_linea_muertes_mensuales(df_mensual):
    # Crear un gráfico de línea con Plotly Express
    fig_lineas = px.line(
        df_mensual,
        x='MES_NOMBRE',  # eje X: nombres de los meses
        y='TOTAL_MUERTES', # eje Y: total de muertes por mes
        markers=True, # eje Y: total de muertes por mes
        labels={'MES_NOMBRE': 'Mes', 'TOTAL_MUERTES': 'Número de muertes'} # etiquetas para los ejes
    )
    return fig_lineas

# Crear grafico de barras
def grafico_barras_ciudades_mas_violentas(df_homicidios):
    # Crear gráfico de barras con Plotly Express
    fig_barras = px.bar(
        df_homicidios,
        x='MUNICIPIO', # eje X: nombre del municipio
        y='TOTAL_HOMICIDIOS', # eje Y: total de homicidios
        text='TOTAL_HOMICIDIOS' # mostrar valores encima de cada barra
    )
    # Ajustar estilo de las barras y posición del texto
    fig_barras.update_traces(
        textposition='outside', # texto fuera de la barra
        marker_color='#6bb9f0' # color azul claro para las barras
    )
    # Configurar diseño del gráfico
    fig_barras.update_layout(
        xaxis=dict(
            showticklabels=True,
            tickfont=dict(size=12),
            title='Municipio'
        ),
        yaxis=dict(
            title='Total Homicidios',
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        title=None,
        margin=dict(l=40, r=20, t=20, b=100)
    )
    return fig_barras

# Crear grafico circular
def grafico_circular_ciudades_menos_mortalidad(df_homicidios):
    # Ordenar y tomar top 10 ciudades con menos homicidios
    ciudades_menos_mortalidad = df_homicidios.sort_values('TOTAL_HOMICIDIOS', ascending=True).head(10)
    # Crear gráfico circular (pie chart)
    fig_circular = px.pie(
        ciudades_menos_mortalidad,
        names='MUNICIPIO',
        values='TOTAL_HOMICIDIOS',
        hole=0, 
    )
    # Configurar texto dentro del gráfico
    fig_circular.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        insidetextorientation='radial'  # mejora orientación texto dentro
    )
    # Ajustar diseño y estilo
    fig_circular.update_layout(
        margin=dict(l=40, r=40, t=60, b=40),
        legend_title_text='Municipios',
        title_x=0.5  # centra el título
    )
    return fig_circular

# Crear grafico tabla
def grafico_tabla_causas_muerte(df_causas):
    # Crear tabla con Plotly para mostrar causas principales de muerte
    fig_tabla = go.Figure(data=[go.Table(
        # Definir ancho de columnas
        columnwidth=[40, 80, 300, 100],
        # Configurar encabezado de la tabla
        header=dict(
            values=["Ranking", "Código de Muerte", "Descripción", "Total Casos"],
            fill_color='#118dff',
            font=dict(family='Work Sans, sans-serif', size=14, color='white'),
            align='center',
            height=50,
        ),
        # Configurar celdas de datos
        cells=dict(
            values=[
                df_causas['RANK'], # ranking de causas
                df_causas['COD_MUERTE'], # código de muerte
                df_causas['DESCRIPCION'], # descripción textual
                df_causas['TOTAL_CASOS'] # total de casos
            ],
            fill_color=[['#f5f8ff', '#e9f0ff'] * 5],  # colores alternados para filas
            font=dict(family='Work Sans, sans-serif', size=13, color='#222'),  # formato texto celdas
            align='center', # centrar texto en celdas
            height=45, # altura de fila datos
            format=[None, None, None, ',d'], # formato numérico para última columna
        )
    )])

    # Ajustar diseño general de la figura
    fig_tabla.update_layout(
        title_x=0.5,
        margin=dict(t=50, b=20, l=10, r=10),
        paper_bgcolor='white',
    )
    return fig_tabla

# Crear grafico histograma
def grafico_histograma_edad(conteo_edad):
    # Crear gráfico de barras para muertes por rango de edad
    fig_histograma = go.Figure(go.Bar(
        x=conteo_edad['RANGO_EDAD'], # Rangos de edad en el eje X
        y=conteo_edad['TOTAL_MUERTES'], # Número de muertes en el eje Y
         marker_color='#6bb9f0'
    ))
    # Configurar títulos y estilo del gráfico
    fig_histograma.update_layout(
        xaxis_title='Rango de Edad (años)',
        yaxis_title='Número de Muertes',
        bargap=0.2
    )
    return fig_histograma

# Crear grafico barras apiladas
def grafico_barras_apiladas_sexo_departamento(conteo_df, depto_col='DEPARTAMENTO', sexo_col='SEXO', valor_col='TOTAL_MUERTES'):
     # Obtener lista ordenada de departamentos y los sexos únicos
    departamentos = sorted(conteo_df[depto_col].unique())
    sexos = conteo_df[sexo_col].unique()

    fig_barras_apiladas = go.Figure()
    # Para cada sexo, agregar una serie de barras con el conteo por departamento
    for sexo in sexos:
        valores = []
        for depto in departamentos:
            fila = conteo_df[(conteo_df[depto_col] == depto) & (conteo_df[sexo_col] == sexo)]
            if not fila.empty:
                valores.append(fila[valor_col].values[0])
            else:
                valores.append(0)  # Si no hay datos, agregar 0 para esa categoría
        fig_barras_apiladas.add_trace(go.Bar(
            x=departamentos,
            y=valores,
            name=str(sexo)
        ))
    # Configurar gráfico para que las barras estén apiladas
    fig_barras_apiladas.update_layout(
        barmode='stack',
        xaxis_title='Departamento',
        yaxis_title='Número de Muertes'
    )

    return fig_barras_apiladas