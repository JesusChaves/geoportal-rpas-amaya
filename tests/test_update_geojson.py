from update_geojson import (
    row_to_geojson_feature,
    merge_features,
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


def test_merge_features_updates_and_appends():
    existing = [
        {"type": "Feature", "properties": {"Nombre": "A", "Valor": 1}},
        {"type": "Feature", "properties": {"Nombre": "B", "Valor": 1}},
    ]
    new = [
        {"type": "Feature", "properties": {"Nombre": "B", "Valor": 2}},
        {"type": "Feature", "properties": {"Nombre": "C", "Valor": 3}},
    ]

    merged = merge_features(existing, new)
    nombres = [f["properties"]["Nombre"] for f in merged]
    valores = [f["properties"].get("Valor") for f in merged]

    assert nombres == ["A", "B", "C"]
    assert valores == [1, 2, 3]

