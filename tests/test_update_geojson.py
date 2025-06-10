import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from update_geojson import (
    row_to_geojson_feature,
    merge_features,
    parse_wkt_polygon,
)


def test_row_to_geojson_feature_returns_valid_geojson():
    row = {
        'COORDENADAS POLIGONO': 'POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))',
        'NOMBRE DE LA MISION': 'Mision1',
        'FECHA': '2023-01-01',
        'LOCALIDAD': 'Sevilla',
        'DESCRIPCION': 'Desc',
        'TAXON': 'Taxon',
        'DEPARTAMENTO': 'Dept',
        'TIPO DE VUELO': 'Tipo',
        'PILOTO': 'Piloto',
        'DRON': 'Dron',
        'SENSOR': 'Sensor',
        'ALTURA DE VUELO (m)': 10,
        'GSD (cm/px)': 5,
        'CONTACTO': 'Contacto',
        'IMAGEN ORTOMOSAICO': 'imagen.png'
    }
    feature = row_to_geojson_feature(row)

    assert isinstance(feature, dict)
    assert feature.get('type') == 'Feature'
    assert 'geometry' in feature
    assert 'properties' in feature


def test_merge_features_adds_new_and_replaces_existing():
    existing = [
        {"type": "Feature", "properties": {"Nombre": "A", "v": 1}},
        {"type": "Feature", "properties": {"Nombre": "B", "old": True}},
    ]
    new = [
        {"type": "Feature", "properties": {"Nombre": "B", "old": False}},
        {"type": "Feature", "properties": {"Nombre": "C"}},
    ]

    merged = merge_features(existing, new)
    nombres = [f["properties"]["Nombre"] for f in merged]

    assert nombres == ["A", "B", "C"]
    assert merged[1]["properties"]["old"] is False


def test_parse_wkt_polygon_with_hole():
    wkt = "POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0), (1 1, 2 1, 2 2, 1 2, 1 1))"
    geom = parse_wkt_polygon(wkt)

    assert geom["type"] == "Polygon"
    assert len(geom["coordinates"]) == 2


def test_parse_wkt_multipolygon():
    wkt = "MULTIPOLYGON (((0 0,1 0,1 1,0 1,0 0)), ((2 2,3 2,3 3,2 3,2 2)))"
    geom = parse_wkt_polygon(wkt)

    assert geom["type"] == "MultiPolygon"
    assert len(geom["coordinates"]) == 2

