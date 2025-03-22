import pandas as pd
import geopandas as gpd
import requests
import json
from io import StringIO

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRcIQQBUKYzfp7AByVKJdj06jXKhUNsypGb97LRDN4L0HgoAHH1YzOY-IG8M8IoN5G5U1AHO0AYNDC8/pub?output=csv"
OUTPUT_FILE = "js/Poligonos_RPAs_AMAYA.js"

def download_google_sheet(sheet_url):
    print("📥 Descargando datos desde Google Sheets...")
    response = requests.get(sheet_url)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text))

def extract_drive_id(url):
    if "id=" in url:
        return url.split("id=")[-1].split("&")[0]
    elif "file/d/" in url:
        return url.split("file/d/")[-1].split("/")[0]
    else:
        return None

def convert_to_geojson(df):
    print("🔄 Convirtiendo datos a GeoJSON...")
    features = []
    for index, row in df.iterrows():
        try:
            coords_str = row["coordenadas"].strip()
            coords = json.loads(coords_str.replace("'", "\""))
            if not isinstance(coords[0][0], list):  # asegurar doble anidamiento
                coords = [coords]

            image_url = row["imagen"]
            image_id = extract_drive_id(image_url)

            if not image_id:
                print(f"🔴 URL mal formateada: {image_url}")
                continue

            thumbnail = f"https://drive.google.com/thumbnail?id={image_id}"

            feature = {
                "type": "Feature",
                "properties": {
                    "mision": row["mision"],
                    "fecha": row["fecha"],
                    "localidad": row["localidad"],
                    "descripcion": row["descripcion"],
                    "operador": row["operador"],
                    "departamento": row["departamento"],
                    "tipo_vuelo": row["tipo_vuelo"],
                    "piloto": row["piloto"],
                    "aeronave": row["aeronave"],
                    "sensor": row["sensor"],
                    "altura": float(row["altura"]),
                    "gsd": float(row["gsd"]),
                    "contacto": row["contacto"],
                    "imagen": thumbnail
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": coords
                }
            }
            features.append(feature)
        except Exception as e:
            print(f"⚠️  Error procesando fila {row.get('mision', index)}: {e}")
            continue

    return {"type": "FeatureCollection", "features": features}

def save_geojson_as_js(geojson, output_file):
    print(f"💾 Guardando archivo en {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("const Poligonos_RPAs_AMAYA = ")
        json.dump(geojson, f, ensure_ascii=False, indent=2)
        f.write(";")
    print(f"✅ Archivo actualizado correctamente.")

def main():
    df = download_google_sheet(SHEET_URL)
    geojson = convert_to_geojson(df)
    save_geojson_as_js(geojson, OUTPUT_FILE)

if __name__ == "__main__":
    main()
