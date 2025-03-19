import pandas as pd
import json
import requests
from shapely import wkt
import io  # ✅ Mueve esto al inicio del script

def download_google_sheet(sheet_url):
    """Descarga datos desde Google Sheets en formato CSV"""
    sheet_csv_url = sheet_url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv")
    response = requests.get(sheet_csv_url)
    
    if response.status_code == 200:
        return pd.read_csv(io.StringIO(response.text))  # ✅ Indentación corregida
    else:
        raise Exception("Error al descargar la hoja de cálculo")  # ✅ Indentación corregida

def convert_to_geojson(df):
    """Convierte los datos de la tabla a GeoJSON"""
    geojson_data = {"type": "FeatureCollection", "features": []}

    for _, row in df.iterrows():
        try:
            # Convertir el polígono desde WKT a GeoJSON
            polygon_geojson = wkt.loads(row["COORDENADAS POLIGONO"])
            
            # Convertir la URL de Google Drive en un enlace visible en la web
            image_url = row["IMAGEN ORTOMOSAICO"] if pd.notna(row["IMAGEN ORTOMOSAICO"]) else ""
            if "drive.google.com" in image_url and "/d/" in image_url:
                try:
                    image_id = image_url.split("/d/")[1].split("/")[0]
                    image_url = f"https://drive.google.com/uc?id={image_id}"
                except IndexError:
                    print(f"⚠️ Error procesando la imagen para {row['NOMBRE DE LA MISION']}: URL incorrecta")
                    image_url = ""  # Deja la imagen en blanco si hay error
            
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
            
            # Agregar entidades al GeoJSON
            geojson_data["features"].append(polygon_feature)
            geojson_data["features"].append(point_feature)
        except Exception as e:
            print(f"Error procesando fila {row['NOMBRE DE LA MISION']}: {e}")
    
    return geojson_data

def save_geojson(geojson_data, output_file):
    """Guarda el archivo GeoJSON en formato JavaScript"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"var poligonosRPAs = {json.dumps(geojson_data, indent=4)};")

if __name__ == "__main__":
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw/edit?usp=sharing"
    OUTPUT_FILE = "Poligonos_RPAs_AMAYA.js"

    df = download_google_sheet(SHEET_URL)
    geojson_data = convert_to_geojson(df)
    save_geojson(geojson_data, OUTPUT_FILE)

    print(f"Archivo {OUTPUT_FILE} actualizado correctamente.")