import pandas as pd
import requests
import json
from shapely import wkt

# URL de la hoja de cálculo de Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw/export?format=csv"

# Archivo de salida (ahora en la carpeta 'js/')
OUTPUT_FILE = "js/Poligonos_RPAs_AMAYA.js"

def download_google_sheet(sheet_url):
    """Descarga datos desde Google Sheets en formato CSV"""
    response = requests.get(sheet_url)
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
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [list(polygon_geojson.exterior.coords)]
                }
            }

            geojson_data["features"].append(polygon_feature)

        except Exception as e:
            print(f"Error procesando fila {row['NOMBRE DE LA MISION']}: {e}")

    return geojson_data

def save_geojson(geojson_data, output_file):
    """Guarda los datos en un archivo JS en la carpeta js/"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("var Poligonos_RPAs_AMAYA = ")
        json.dump(geojson_data, f, indent=4, ensure_ascii=False)

def main():
    """Ejecuta el proceso de conversión y guardado"""
    df = download_google_sheet(SHEET_URL)
    geojson_data = convert_to_geojson(df)
    save_geojson(geojson_data, OUTPUT_FILE)
    print(f"Archivo {OUTPUT_FILE} actualizado correctamente.")

if __name__ == "__main__":
    main()

