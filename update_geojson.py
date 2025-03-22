import pandas as pd
import geopandas as gpd
import json
import requests
from shapely import wkt
from pathlib import Path

# URL del Google Sheet exportado como CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw/export?format=csv"

# Ruta donde se guardará el archivo JS
OUTPUT_FILE = Path("js/Poligonos_RPAs_AMAYA.js")

def download_google_sheet(url):
    print("📥 Descargando datos desde Google Sheets...")
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(pd.compat.StringIO(response.text))

def validate_image_url(url):
    if not isinstance(url, str) or "drive.google.com" not in url or "id=" not in url:
        return False
    return True

def convert_row_to_feature(row):
    try:
        geometry = wkt.loads(row["geometry"])
        if geometry.geom_type != "Polygon":
            print(f"⚠️  Geometría no válida en fila {row['mision']}: {geometry.geom_type}")
            return None
        if not validate_image_url(row["imagen_ortomosaico"]):
            print(f"🔴 URL mal formateada: {row['imagen_ortomosaico']}")
            return None
        return {
            "type": "Feature",
            "properties": {
                "mision": row["mision"],
                "fecha": row["fecha"],
                "localidad": row["localidad"],
                "provincia": row["provincia"],
                "area": row["area"],
                "cultivo": row["cultivo"],
                "descripcion": row["descripcion"],
                "vuelos": row["vuelos"],
                "resolucion": row["resolucion"],
                "gcp": row["gcp"],
                "restituido": row["restituido"],
                "observaciones": row["observaciones"],
                "imagen": row["imagen_ortomosaico"]
            },
            "geometry": json.loads(gpd.GeoSeries([geometry]).to_json())["features"][0]["geometry"]
        }
    except Exception as e:
        print(f"❌ Error procesando fila {row.get('mision', '???')}: {e}")
        return None

def save_geojson_js(features, output_file):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "type": "FeatureCollection",
        "features": features
    }
    js_variable = f"const Poligonos_RPAs_AMAYA = {json.dumps(data, indent=4)};"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(js_variable)
    print(f"✅ Archivo actualizado correctamente: {output_file}")

def main():
    df = download_google_sheet(SHEET_URL)
    print("🔄 Convirtiendo datos a GeoJSON...")
    features = []

    for _, row in df.iterrows():
        feature = convert_row_to_feature(row)
        if feature:
            features.append(feature)

    save_geojson_js(features, OUTPUT_FILE)

if __name__ == "__main__":
    main()

