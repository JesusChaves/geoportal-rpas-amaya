# update_geojson.py
import pandas as pd
import requests
import json

# URL para exportar tu sheet como CSV
SHEET_ID = '1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw'
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Lee la información desde el Google Sheet
df = pd.read_csv(CSV_URL)

# Función que transforma cada registro del Sheet a un Feature GeoJSON
def row_to_geojson_feature(row):
    coords = json.loads(row['GeoJSON'])  # Suponiendo que tienes una columna llamada GeoJSON con la geometría
    properties = {
        "Nombre": row['Nombre de la misión'],
        "Fecha": row['Fecha'],
        "Localidad": row['Localidad'],
        "Descripcion": row['Descripcion'],
        "Taxon": row['Taxón'],
        "Departamento": row['Departamento'],
        "Tipo_Vuelo": row['Tipo de Vuelo'],
        "Piloto": row['Piloto'],
        "Dron": row['Dron'],
        "Sensor": row['Sensor'],
        "Altura_Vuelo": row['Altura de Vuelo (m)'],
        "GSD": row['GSD (cm/px)'],
        "Contacto": row['Contacto'],
        "Imagen": row['URL_imagen']  # Asume una columna con URL de imagen
    }
    return {
        "type": "Feature",
        "geometry": coords,
        "properties": properties
    }

# Convierte el DataFrame en GeoJSON FeatureCollection
features = [row_to_geojson_feature(row) for idx, row in df.iterrows()]

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Guarda el archivo GeoJSON
with open('Poligonos_RPAS.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print("GeoJSON actualizado correctamente.")
