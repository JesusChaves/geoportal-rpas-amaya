# update_geojson.py
import os
from pathlib import Path
import csv
import json


def _num_or_str(value):
    """Convierte valores numéricos en float si es posible."""
    try:
        if value is None or value == "" or str(value).lower() == "n/a" or str(value) == "-":
            return value
        return float(value)
    except ValueError:
        return value

# Ruta al GeoJSON en disco
GEOJSON_PATH = "Poligonos_RPAS.json"

# Ruta al CSV local
CSV_PATH = Path(__file__).parent / "Geodatabase" / "Geodatabase.csv"

# Función que transforma cada registro del Sheet a un Feature GeoJSON
def parse_wkt_polygon(wkt_text: str):
    """Convierte WKT de tipo POLYGON o MULTIPOLYGON a coordenadas GeoJSON."""

    def _extract_parts(text: str):
        """Extrae secciones entre paréntesis al primer nivel."""
        parts = []
        depth = 0
        start = None
        for i, ch in enumerate(text):
            if ch == '(':  # nueva subsección
                if depth == 0:
                    start = i + 1
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0 and start is not None:
                    parts.append(text[start:i])
            elif ch == ',' and depth == 0:
                # separador entre polígonos o anillos
                continue
        if not parts and text:
            parts.append(text)
        return parts

    def _parse_ring(ring_text: str):
        coords = []
        for part in ring_text.split(','):
            x_str, y_str = part.strip().split()[:2]
            coords.append([float(x_str), float(y_str)])
        return coords

    try:
        text = wkt_text.strip()
        upper = text.upper()

        if upper.startswith('MULTIPOLYGON'):
            text = text[len('MULTIPOLYGON'):].strip()
            if text.startswith('(') and text.endswith(')'):
                text = text[1:-1]
            polygon_texts = _extract_parts(text)
            multipoly = []
            for poly_text in polygon_texts:
                rings_texts = _extract_parts(poly_text)
                rings = [_parse_ring(r) for r in rings_texts]
                multipoly.append(rings)
            return {"type": "MultiPolygon", "coordinates": multipoly}
        else:
            if upper.startswith('POLYGON'):
                text = text[len('POLYGON'):].strip()
            if text.startswith('(') and text.endswith(')'):
                text = text[1:-1]
            rings_texts = _extract_parts(text)
            rings = [_parse_ring(r) for r in rings_texts]
            return {"type": "Polygon", "coordinates": rings}
    except Exception as e:
        raise ValueError(f"Error al parsear WKT: {e}")


def row_to_geojson_feature(row):
    try:
        geom_wkt = row['COORDENADAS POLIGONO']
        coords = parse_wkt_polygon(geom_wkt)
    except Exception as e:
        print(f"Fila ignorada por error WKT: {e} - fila: {row}")
        return None

    properties = {
        "Nombre": row.get('NOMBRE DE LA MISION'),
        "Fecha": row.get('FECHA'),
        "Localidad": row.get('LOCALIDAD'),
        "Descripcion": row.get('DESCRIPCION'),
        "Taxon": row.get('TAXON'),
        "Departamento": row.get('DEPARTAMENTO'),
        "Tipo_Vuelo": row.get('TIPO DE VUELO'),
        "Piloto": row.get('PILOTO'),
        "Dron": row.get('DRON'),
        "Sensor": row.get('SENSOR'),
        "Altura_Vuelo": _num_or_str(row.get('ALTURA DE VUELO (m)')),
        "GSD": _num_or_str(row.get('GSD (cm/px)')),
        "Contacto": row.get('CONTACTO'),
        "Imagen": row.get('IMAGEN ORTOMOSAICO')
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

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        new_features = []
        for row in reader:
            feature = row_to_geojson_feature(row)
            if feature is not None:
                new_features.append(feature)

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
