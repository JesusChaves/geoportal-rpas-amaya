# update_geojson.py
import os
import pandas as pd
import requests
import json
import io
from shapely import wkt
import shapely.geometry

# Ruta al GeoJSON en disco
GEOJSON_PATH = "Poligonos_RPAS.json"

# URL o identificador del Sheet.
# Se obtiene de la variable de entorno ``SHEET_ID`` y se
# utiliza un valor por defecto si dicha variable no está definida.
SHEET_ID = os.getenv("SHEET_ID") or "1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw"

# ``SHEET_ID`` puede contener la URL completa al CSV o solo el identificador
# del documento de Google Sheets. En este último caso se construye la ruta de
# exportación a CSV.
CSV_URL = (
    SHEET_ID
    if SHEET_ID.startswith("http")
    else f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
)

# Tiempo máximo de espera para la descarga del CSV (en segundos)
TIMEOUT = 10

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


def load_existing_features(path: str = GEOJSON_PATH):
    """Carga los features existentes desde un archivo GeoJSON."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("features", [])
    except (OSError, json.JSONDecodeError):
        return []


def merge_features(existing, new):
    """Combina listas de features evitando duplicados por nombre."""
    names = {f.get("properties", {}).get("Nombre") for f in existing}
    merged = list(existing)
    for feat in new:
        name = feat.get("properties", {}).get("Nombre")
        if name not in names:
            merged.append(feat)
            names.add(name)
    return merged

def update_geojson():
    """Descarga el CSV de Google Sheets y actualiza el GeoJSON existente."""
    try:
        resp = requests.get(CSV_URL, timeout=TIMEOUT)
        if resp.status_code != 200:
            print(f"Error al descargar el CSV: código HTTP {resp.status_code}")
            return
    except requests.RequestException as e:
        print(f"Error de red al descargar el CSV: {e}")
        return

    df = pd.read_csv(io.StringIO(resp.text))

    # Features nuevos a partir del sheet
    new_features = [row_to_geojson_feature(row) for idx, row in df.iterrows()]
    new_features = [feature for feature in new_features if feature is not None]

    # Carga los existentes y combínalos
    existing = load_existing_features(GEOJSON_PATH)
    merged = merge_features(existing, new_features)

    geojson = {
        "type": "FeatureCollection",
        "features": merged
    }

    with open(GEOJSON_PATH, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print("GeoJSON actualizado correctamente.")


if __name__ == "__main__":
    update_geojson()
