import pandas as pd
import requests
import json
import os
from shapely import wkt

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
            # Validar que la columna de coordenadas no esté vacía
            if pd.isna(row["COORDENADAS POLIGONO"]):
                print(f"Error: Registro {row['mision']} no tiene coordenadas.")
                continue
            
            # Convertir el polígono desde WKT a GeoJSON
            polygon_geojson = wkt.loads(row["COORDENADAS POLIGONO"])
            
            # Manejo de la imagen para asegurar que es un enlace válido
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
                    "imagen": image_url
                },
                "geometry": polygon_geojson
            }
            
            geojson_data["features"].append(polygon_feature)
        except Exception as e:
            print(f"Error procesando fila {row['mision']}: {e}")
    
    return geojson_data

def save_geojson(geojson_data, output_path):
    """Guarda los datos en formato .js en la carpeta js/"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"const Poligonos_RPAs_AMAYA = {json.dumps(geojson_data, indent=4, ensure_ascii=False)};")

def main():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw/edit?usp=sharing"
    print("Descargando datos desde Google Sheets...")
    df = download_google_sheet(SHEET_URL)
    print("Convirtiendo datos a GeoJSON...")
    geojson_data = convert_to_geojson(df)
    output_file = "js/Poligonos_RPAs_AMAYA.js"
    save_geojson(geojson_data, output_file)
    print(f"Archivo {output_file} actualizado correctamente.")

if __name__ == "__main__":
    main()
