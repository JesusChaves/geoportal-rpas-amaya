import pandas as pd
import requests
import geopandas as gpd
import shapely.wkt
import shapely.geometry

# URL de la hoja de Google Sheets en formato CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw/gviz/tq?tqx=out:csv"

def download_google_sheet(sheet_url):
    """Descarga los datos de Google Sheets en formato CSV"""
    response = requests.get(sheet_url)
    
    if response.status_code == 200:
        return pd.read_csv(pd.compat.StringIO(response.text))
    else:
        raise Exception(f"❌ Error al descargar la hoja de cálculo: {response.status_code}")

def convert_to_geojson(df):
    """Convierte los datos de la tabla en formato GeoJSON"""
    geojson_data = {"type": "FeatureCollection", "features": []}

    for _, row in df.iterrows():
        try:
            # Verificar si las coordenadas están presentes y no vacías
            if "COORDENADAS POLIGONO" not in row or pd.isna(row["COORDENADAS POLIGONO"]):
                print(f"⚠️ Error en fila {row.get('NOMBRE DE LA MISION', 'SIN IDENTIFICADOR')}: Coordenadas no disponibles")
                continue

            # Convertir WKT a GeoJSON
            try:
                polygon_geojson = shapely.wkt.loads(row["COORDENADAS POLIGONO"])
            except Exception as e:
                print(f"⚠️ Error en fila {row.get('NOMBRE DE LA MISION', 'SIN IDENTIFICADOR')}: {e}")
                continue

            # Procesar URL de imagen
            image_url = row["IMAGEN ORTOMOSAICO"] if pd.notna(row["IMAGEN ORTOMOSAICO"]) else ""
            if "drive.google.com" in image_url:
                try:
                    image_id = image_url.split("/d/")[1].split("/")[0]
                    image_url = f"https://drive.google.com/uc?id={image_id}"
                except IndexError:
                    print(f"⚠️ Error en fila {row.get('NOMBRE DE LA MISION', 'SIN IDENTIFICADOR')}: URL de imagen incorrecta")
                    image_url = ""

            # Crear estructura del polígono en GeoJSON
            polygon_feature = {
                "type": "Feature",
                "properties": {
                    "mision": row.get("NOMBRE DE LA MISION", "SIN NOMBRE"),
                    "fecha": row.get("FECHA", "SIN FECHA"),
                    "localidad": row.get("LOCALIDAD", "SIN LOCALIDAD"),
                    "descripcion": row.get("DESCRIPCION", "SIN DESCRIPCION"),
                    "operador": row.get("OPERADOR", "SIN OPERADOR"),
                    "departamento": row.get("DEPARTAMENTO", "SIN DEPARTAMENTO"),
                    "tipo_vuelo": row.get("TIPO VUELO", "SIN TIPO VUELO"),
                    "piloto": row.get("PILOTO", "SIN PILOTO"),
                    "aeronave": row.get("AERONAVE", "SIN AERONAVE"),
                    "sensor": row.get("SENSOR", "SIN SENSOR"),
                    "altura": row.get("ALTURA", "SIN ALTURA"),
                    "gsd": row.get("GSD", "SIN GSD"),
                    "contacto": row.get("CONTACTO", "SIN CONTACTO"),
                    "imagen": image_url
                },
                "geometry": shapely.geometry.mapping(polygon_geojson)
            }
            
            geojson_data["features"].append(polygon_feature)

        except Exception as e:
            print(f"❌ Error inesperado en fila {row.get('NOMBRE DE LA MISION', 'SIN IDENTIFICADOR')}: {e}")
    
    return geojson_data

def save_geojson(data, output_path="js/Poligonos_RPAs_AMAYA.js"):
    """Guarda el GeoJSON en un archivo JS"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"const Poligonos_RPAs_AMAYA = {data};")

def main():
    print("📥 Descargando datos desde Google Sheets...")
    df = download_google_sheet(SHEET_URL)

    print("🌍 Convirtiendo datos a GeoJSON...")
    geojson_data = convert_to_geojson(df)

    print(f"💾 Guardando archivo en js/Poligonos_RPAs_AMAYA.js...")
    save_geojson(geojson_data)

    print("✅ Archivo actualizado correctamente.")

if __name__ == "__main__":
    main()
