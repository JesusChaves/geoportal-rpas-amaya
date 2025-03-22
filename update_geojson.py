import pandas as pd
import requests
from shapely import wkt
import json
import io

# URL de la hoja de cálculo
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw/export?format=csv"

def download_google_sheet(sheet_url):
    """Descarga una hoja de cálculo de Google Sheets como DataFrame"""
    print("📥 Descargando datos desde Google Sheets...")
    response = requests.get(sheet_url)
    if response.status_code == 200:
        return pd.read_csv(io.StringIO(response.text))
    else:
        raise Exception("Error al descargar la hoja de cálculo")

def convert_to_geojson(df):
    """Convierte los datos de la tabla a GeoJSON"""
    print("🔄 Convirtiendo datos a GeoJSON...")
    geojson_data = {"type": "FeatureCollection", "features": []}

    for _, row in df.iterrows():
        try:
            # Convertir el polígono desde WKT a GeoJSON
            polygon_geojson = wkt.loads(row["COORDENADAS POLIGONO"])

            # Convertir la URL de Google Drive en un enlace visible
            image_url = row["IMAGEN ORTOMOSAICO"] if pd.notna(row["IMAGEN ORTOMOSAICO"]) else ""
            if "drive.google.com" in image_url:
                try:
                    image_id = image_url.split("/d/")[1].split("/")[0]
                    image_url = f"https://drive.google.com/uc?id={image_id}"
                    print(f"🟢 ID de imagen extraído: {image_id}")
                except IndexError:
                    print(f"🔴 URL mal formateada: {image_url}")
                    continue
            else:
                print(f"🟡 URL no es de Google Drive: {image_url}")
                continue

            # Crear la entidad del polígono
            polygon_feature = {
                "type": "Feature",
                "properties": {
                    "mision": row["NOMBRE DE LA MISION"],
                    "fecha": row["FECHA"],
                    "localidad": row["LOCALIDAD"],
                    "descripcion": row["DESCRIPCION"],
                    "operador": row["OPERADOR"],
                    "departamento": row["DEPARTAMENTO"],
                    "tipo_vuelo": row["TIPO VUELO"],
                    "piloto": row["PILOTO"],
                    "aeronave": row["AERONAVE"],
                    "sensor": row["SENSOR"],
                    "altura": row["ALTURA"],
                    "gsd": row["GSD"],
                    "contacto": row["CONTACTO"],
                    "imagen": image_url
                },
                "geometry": json.loads(json.dumps(polygon_geojson.__geo_interface__))
            }

            geojson_data["features"].append(polygon_feature)

        except Exception as e:
            print(f"❌ Error procesando fila {row['NOMBRE DE LA MISION']}: {e}")

    return geojson_data

def save_geojson(geojson_data, output_path="js/Poligonos_RPAs_AMAYA.js"):
    """Guarda los datos GeoJSON como archivo JS"""
    print(f"💾 Guardando archivo en {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("const Poligonos_RPAs_AMAYA = ")
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)
        f.write(";")
    print("✅ Archivo actualizado correctamente.")

def main():
    df = download_google_sheet(SHEET_URL)
    geojson_data = convert_to_geojson(df)
    save_geojson(geojson_data)

if __name__ == "__main__":
    main()
