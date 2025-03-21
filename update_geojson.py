import pandas as pd
import requests
import json
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
            # Verificar si la columna de coordenadas no está vacía
            if pd.isna(row["COORDENADAS POLIGONO"]):
                print(f"⚠️ Advertencia: La fila {_} no tiene coordenadas y será omitida.")
                continue
            
            # Convertir el polígono desde WKT a GeoJSON
            polygon_geojson = wkt.loads(row["COORDENADAS POLIGONO"])
            
            # Manejar URLs de imágenes
            image_url = row["IMAGEN ORTOMOSAICO"] if pd.notna(row["IMAGEN ORTOMOSAICO"]) else ""
            if "drive.google.com" in image_url:
                try:
                    image_id = image_url.split("/d/")[1].split("/")[0]
                    image_url = f"https://drive.google.com/uc?id={image_id}"
                except IndexError:
                    print(f"⚠️ Error procesando imagen en fila {_}: URL incorrecta")
                    image_url = ""
            
            # Crear entidad GeoJSON
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
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [list(polygon_geojson.exterior.coords)]
                }
            }
            
            geojson_data["features"].append(polygon_feature)
            print(f"✅ Procesando fila {_}: {row['NOMBRE DE LA MISION']}")
        except Exception as e:
            print(f"❌ Error procesando fila {row['NOMBRE DE LA MISION']}: {e}")
    
    return geojson_data

def save_geojson(data, output_file):
    """Guarda los datos en un archivo JSON"""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"📁 Archivo {output_file} actualizado correctamente.")

def main():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw/edit?usp=sharing"
    OUTPUT_FILE = "js/Poligonos_RPAs_AMAYA.js"
    
    print("🔄 Descargando datos desde Google Sheets...")
    df = download_google_sheet(SHEET_URL)
    
    print("🌍 Convirtiendo datos a GeoJSON...")
    geojson_data = convert_to_geojson(df)
    
    print("💾 Guardando archivo GeoJSON...")
    save_geojson(geojson_data, OUTPUT_FILE)
    
    print("✅ Proceso completado.")

if __name__ == "__main__":
    main()
