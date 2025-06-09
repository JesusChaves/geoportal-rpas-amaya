import pandas as pd
from update_geojson import row_to_geojson_feature


def test_row_to_geojson_feature_returns_valid_geojson():
    data = {
        'COORDENADAS POLIGONO': ['POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))'],
        'NOMBRE DE LA MISION': ['Mision1'],
        'FECHA': ['2023-01-01'],
        'LOCALIDAD': ['Sevilla'],
        'DESCRIPCION': ['Desc'],
        'TAXON': ['Taxon'],
        'DEPARTAMENTO': ['Dept'],
        'TIPO DE VUELO': ['Tipo'],
        'PILOTO': ['Piloto'],
        'DRON': ['Dron'],
        'SENSOR': ['Sensor'],
        'ALTURA DE VUELO (m)': [10],
        'GSD (cm/px)': [5],
        'CONTACTO': ['Contacto'],
        'IMAGEN ORTOMOSAICO': ['imagen.png']
    }
    df = pd.DataFrame(data)
    feature = row_to_geojson_feature(df.iloc[0])

    assert isinstance(feature, dict)
    assert feature.get('type') == 'Feature'
    assert 'geometry' in feature
    assert 'properties' in feature

