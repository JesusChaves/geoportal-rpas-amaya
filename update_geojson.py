# update_geojson.py
import pandas as pd
import requests
import json
import io
from shapely import wkt
import shapely.geometry

# URL para exportar tu sheet como CSV
SHEET_ID = '1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw'
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Función que transforma cada registro del Sheet a un Feature GeoJSON
def row_to_geojson_feature(row):
    try:
        geom_wkt = row['COORDENADAS POLIGONO']
        shape = wkt.loads(geom_wkt)
        coords = shapely.geometry.mapping(shape)
    except Exception as e:
        print(f"Fila ignorada por error WKT: {e} - fila: {row}")
        return None

    properties = {
        "Nombre": row['NOMBRE DE LA MISION'],
        "Fecha": row['FECHA'],
        "Localidad": row['LOCALIDAD'],
        "Descripcion": row['DESCRIPCION'],
        "Taxon": row['TAXON'],
        "Departamento": row['DEPARTAMENTO'],
        "Tipo_Vuelo": row['TIPO DE VUELO'],
        "Piloto": row['PILOTO'],
        "Dron": row['DRON'],
        "Sensor": row['SENSOR'],
        "Altura_Vuelo": row['ALTURA DE VUELO (m)'],
        "GSD": row['GSD (cm/px)'],
        "Contacto": row['CONTACTO'],
        "Imagen": row['IMAGEN ORTOMOSAICO']
    }
    return {
        "type": "Feature",
        "geometry": coords,
        "properties": properties
    }

def update_geojson():
    """Descarga el CSV de Google Sheets y genera el GeoJSON."""
    try:
        resp = requests.get(CSV_URL, timeout=10)
        if resp.status_code != 200:
            print(f"Error al descargar el CSV: codigo {resp.status_code}")
            return
    except requests.RequestException as e:
        print(f"Error de red al descargar el CSV: {e}")
        return

    df = pd.read_csv(io.StringIO(resp.text))

    # Convierte el DataFrame en GeoJSON FeatureCollection
    features = [row_to_geojson_feature(row) for idx, row in df.iterrows()]
    features = [feature for feature in features if feature is not None]

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # Guarda el archivo GeoJSON como .json (para uso en la web)
    with open('Poligonos_RPAS.json', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print("GeoJSON actualizado correctamente.")


if __name__ == "__main__":
    update_geojson()
