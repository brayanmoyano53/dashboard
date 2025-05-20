import json
from pathlib import Path
import pandas as pd


# Obtener la ruta base del proyecto (2 niveles arriba desde este archivo)
DATA_DIR = Path(__file__).parent.parent / 'data'

def cargar_datos_mortalidad():
    ruta = DATA_DIR / 'datosmortalidad.csv'
    return pd.read_csv(ruta, encoding='latin1')

def cargar_division_politico_administrativa():
    ruta = DATA_DIR / 'divipola.csv'
    return pd.read_csv(ruta, encoding='latin1')

def cargar_codigos_de_muerte():
    ruta = DATA_DIR / 'Codigosmuerte.csv'
    return pd.read_csv(ruta, encoding='latin1')

def cargar_geojson_colombia():
    ruta = DATA_DIR / 'Colombia.geo.json'
    with open(ruta, 'r', encoding='utf-8') as f:
        geojson = json.load(f)
    return geojson
