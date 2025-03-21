import requests
import pandas as pd
import json
import io
from shapely import wkt

# URL de la hoja de cálculo de Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw/edit?usp=sharing"

def download_google_sheet(sheet_url):
    """Descarga datos desde Google Sheets en formato CSV"""
    sheet_csv_url = sheet_url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv")
    response = requests.get(sheet_csv_url)

    if response.status_code == 200:
        return pd.read_csv(io.StringIO(response.text))  # Corrección aplicada aquí
    else:
        raise Exception("Error al descargar la hoja de cálculo")

def convert_to_geojson(df):
    """Convierte los datos de la tabla a GeoJSON"""
    geojson_data = {"type": "FeatureCollection", "features": []}

    for _, row in df.iterrows():
        try:
            # Convertir el polígono desde WKT a GeoJSON
            polygon_geojson = wkt.loads(row["COORDENADAS POLIGONO"])

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
                    "operador": row["OPERADOR"],
                    "departamento": row["DEPARTAMENTO"],
                    "tipo_vuelo": row["TIPO DE VUELO"],
                    "piloto": row["PILOTO"],
                    "aeronave": row["AERONAVE"],
                    "sensor": row["SENSOR"],
                    "altura": row["ALTURA"],
                    "gsd": row["GSD"],
                    "contacto": row["CONTACTO"],
                    "imagen": image_url,
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates

