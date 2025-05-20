import sys
import os
import json 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Importamos las clases y funciones necesarias del framework Dash para construir la app web
from dash import Dash, dcc, html, Input, Output,dash_table

# Importamos nuestros módulos personalizados para manejar los datos y gráficos
# 'cargar_datos' para cargar los datos desde archivos o fuentes externas
# 'procesar_datos' para realizar el procesamiento y análisis de los datos
# 'generar_graficos' para crear visualizaciones con plotly u otras librerías
from src.modulos import cargar_datos, procesar_datos, generar_graficos

# Creamos la instancia de la aplicación Dash, que será la base de nuestra app web.
# Obtenemos el objeto Flask para poder integrarlo con servidores web
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Cargar datos de los archivos de mortalidad,division politico-administrativa, codigos de muerte y geojson para el mapa
df_mortalidad = cargar_datos.cargar_datos_mortalidad()
df_division = cargar_datos.cargar_division_politico_administrativa()
df_codigos = cargar_datos.cargar_codigos_de_muerte()
counties = cargar_datos.cargar_geojson_colombia()
# procesamos solo los datos del año 2019
df_2019 = procesar_datos.filtrar_año(df_mortalidad, 2019)

# Procesar datos para mapa: Visualización de la distribución total de muertes por departamento en Colombia para el año 2019.
muertes = procesar_datos.agrupar_muertes_por_departamento(df_2019)
departamentos = procesar_datos.obtener_departamentos_mas_frecuentes(df_division)
vista_mapa = procesar_datos.merge_muertes_departamentos(muertes, departamentos)
# Procesar datos para gráfico de líneas: Representación del total de muertes por mes en Colombia, mostrando variaciones a lo largo del año.
muertes_mensuales = procesar_datos.agrupar_muertes_por_mes(df_2019)
# Procesar datos para gráfico de barras: Visualización de las 5 ciudades más violentas de Colombia, considerando homicidios (códigos X95)
ciudades_mas_violentas = procesar_datos.ciudades_mas_violentas(df_2019, df_division)

# Generar grafico para mapa: Visualización de la distribución total de muertes por departamento en Colombia para el año 2019.
fig_mapa_colombia = generar_graficos.crear_mapa(
    counties_geojson=counties,
    locs=vista_mapa['COD_DEPARTAMENTO'],
    valores=vista_mapa['TotalMuertes'],
    textos=vista_mapa['DEPARTAMENTO']
)
# Generar gráfico de líneas: Representación del total de muertes por mes en Colombia, mostrando variaciones a lo largo del año.
fig_grafico_lineas = generar_graficos.grafico_linea_muertes_mensuales(muertes_mensuales)
# Generar gráfico de barras: Visualización de las 5 ciudades más violentas de Colombia, considerando homicidios (códigos X95)
fig_grafico_barras = generar_graficos.grafico_barras_ciudades_mas_violentas(ciudades_mas_violentas)

# Definiendo el estilo html y las paginas para cada una de las figuras
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Header([
        html.Div([
            html.Span("🇨🇴", style={"fontSize": "32px", "marginRight": "10px", "verticalAlign": "middle"}),
            html.H1("MORTALIDAD EN COLOMBIA", className="logo", style={"display": "inline-block", "verticalAlign": "middle"}),
            html.Nav([
                html.Ul([
                    html.Li(html.A("MAPA", href="/mapa")),
                    html.Li(html.A("LÍNEAS", href="/lineas")),
                    html.Li(html.A("BARRAS", href="/barras")),
                    html.Li(html.A("CIRCULAR", href="/circular")),
                    html.Li(html.A("TABLA", href="/tabla")),
                    html.Li(html.A("HISTOGRAMA", href="/histograma")),
                    html.Li(html.A("BARRAS APILADAS", href="/apiladas")),
                ])
            ])
        ], className="container")
    ]),

    html.Div(id='page-content', className="container"),
    html.Script('''
        function sendHeight() {
            var height = document.body.scrollHeight;
            window.parent.postMessage({iframeHeight: height}, '*');
        }
        window.onload = sendHeight;
        window.onresize = sendHeight;
    ''')
])

# Página 1 - Mapa
layout_mapa = html.Div([
    html.H2("Mapa de Muertes Totales por Departamento en Colombia (2019)", style={'textAlign': 'center'}),
    dcc.Graph(id='mapa-mortalidad', figure=fig_mapa_colombia, style={'width': '100%', 'height': '750px'})
])

# Página 2 - Gráfico de líneas
layout_lineas = html.Div([
    html.H2("Variación Mensual del Total de Muertes en Colombia (2019)", style={'textAlign': 'center'}),
    dcc.Graph(id='grafico-lineas', figure=fig_grafico_lineas, style={'width': '100%', 'height': '750px'})
])
# Página 3 - Gráfico de barras
layout_barras = html.Div([
    html.H2("Top 5 Ciudades Más Violentas en Colombia por Homicidios (2019)", style={'textAlign': 'center'}),
    dcc.Graph(id='grafico-barras', figure=fig_grafico_barras, style={'width': '100%', 'height': '750px'})
])



# Callback de enrutamiento
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def mostrar_contenido(pathname):
    if pathname == "/mapa":
        return layout_mapa
    elif pathname == "/lineas":
        return layout_lineas
    elif pathname == "/barras":
        return layout_barras
    else:
        return layout_mapa  # Pagina inicial mapa

# Esto permite correr localmente
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Render establece el puerto en esta variable
    app.run(host="0.0.0.0", port=port)