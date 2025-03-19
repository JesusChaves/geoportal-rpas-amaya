import pandas as pd
import json
import requests
from shapely import wkt
import os

def download_google_sheet(sheet_url):
    """Descarga datos desde Google Sheets en formato CSV"""
    sheet_csv_url = sheet_url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv")
    response = requests.get(sheet_csv_url)
    if response.status_code == 200:
        return pd.read_csv(pd.compat.StringIO(response.text))
    else:
        raise Exception("Error al descargar la hoja de cálculo")

def convert_to_geojson(df):
    """Convierte los datos de la tabla a GeoJSON"""
    geojson_data = {"type": "FeatureCollection", "features": []}

for _, row in df.iterrows():
    try:
        polygon_geojson = wkt.loads(row["POLIGONO"])

        point_feature = {
            "type": "Feature",
            "properties": {
                "mision": row["NOMBRE DE LA MISION"],
                "fecha": row["FECHA"],
                "localidad": row["LOCALIDAD"],
                "descripcion": row["DESCRIPCION"],
                "operador": row["OPERADOR UAS"],
                "departamento": row["DEPARTAMENTO"],
                "tipo_vuelo": row["TIPO DE VUELO"],
                "piloto": row["PILOTO"],
                "aeronave": row["DRONE"],
                "sensor": row["SENSOR"],
                "altura": row["ALTURA DE VUELO (m)"],
                "gsd": row["GSD (cm/px)"],
                "contacto": row["CONTACTO"],
                "imagen": row["IMAGEN ORTOMOSAICO"]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row["LONGITUD"], row["LATITUD"]]
            }
        }

    except Exception as e:
        print(f"Error procesando fila {row['NOMBRE DE LA MISION']}: {e}")

            # Crear entidad de punto central
point_feature = {
    "type": "Feature",
    "properties": polygon_feature["properties"],
    "geometry": {
        "type": "Point",
        "coordinates": [row["LONGITUD"], row["LATITUD"]]
    }
}
