# update_geojson.py
import os
from pathlib import Path
import pandas as pd
import json
from shapely import wkt
import shapely.geometry

# Ruta al GeoJSON en disco
GEOJSON_PATH = "Poligonos_RPAS.json"

# Ruta al CSV local
CSV_PATH = Path(__file__).parent / "Geodatabase" / "Geodatabase.csv"

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
    """Carga el CSV local y actualiza el GeoJSON existente."""
    if not CSV_PATH.exists():
        print(f"No se encontró el archivo CSV en {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)

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
