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
            # Convertir el polígono desde WKT a GeoJSON
            polygon_geojson = wkt.loads(row["POLIGONO"])

            # Convertir la URL de Google Drive en un enlace visible en la web
            image_url = row["IMAGEN ORTOMOSAICO"] if pd.notna(row["IMAGEN ORTOMOSAICO"]) else ""
            if "drive.google.com" in image_url:
                image_id = image_url.split("/d/")[1].split("/")[0]
                image_url = f"https://drive.google.com/uc?id={image_id}"

            # Crear entidad de polígono
            polygon_feature = {
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
                    "imagen": image_url
                },
                "geometry": json.loads(json.dumps(polygon_geojson.__geo_interface__))
            }

            # Crear entidad de punto central
point_feature = {
    "type": "Feature",
    "properties": polygon_feature["properties"],
    "geometry": {
        "type": "Point",
        "coordinates": [row["LONGITUD"], row["LATITUD"]]
    }
}
