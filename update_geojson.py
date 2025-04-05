# update_geojson.py
import pandas as pd
import requests
import json
from shapely import wkt
import shapely.geometry

# URL para exportar tu sheet como CSV
SHEET_ID = '1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw'
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Lee la información desde el Google Sheet
df = pd.read_csv(CSV_URL)

# Función que transforma cada registro del Sheet a un Feature GeoJSON
def row_to_geojson_feature(row):
    try:
        geom_wkt = row['COORDENADAS POLIGONO']
        shape = wkt.loads(geom_wkt)
        coords = shapely.geometry.mapping(shape)
    except Exception as e:
        print(f"Fila ignorada por error WKT: {e} - fila: {row}")
        return None

    properties = {
        "Nombre": row['NOMBRE DE LA MISION'],
        "Fecha": row['FECHA'],
        "Localidad": row['LOCALIDAD'],
        "Descripcion": row['DESCRIPCION'],
        "Taxon": row['TAXON'],
        "Departamento": row['DEPARTAMENTO'],
        "Tipo_Vuelo": row['TIPO DE VUELO'],
        "Piloto": row['PILOTO'],
        "Dron": row['DRON'],
        "Sensor": row['SENSOR'],
        "Altura_Vuelo": row['ALTURA DE VUELO (m)'],
        "GSD": row['GSD (cm/px)'],
        "Contacto": row['CONTACTO'],
        "Imagen": row['IMAGEN ORTOMOSAICO']
    }
    return {
        "type": "Feature",
        "geometry": coords,
        "properties": properties
    }

# Convierte el DataFrame en GeoJSON FeatureCollection
features = [row_to_geojson_feature(row) for idx, row in df.iterrows()]
features = [feature for feature in features if feature is not None]

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Guarda el archivo GeoJSON
with open('Poligonos_RPAS.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print("GeoJSON actualizado correctamente.")
