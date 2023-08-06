from pathlib import Path

from tests.test_all import test_function

from geoformat_lib.conf.path import (
    add_extension_path,
    path_to_file_path
)

add_extension_path_parameters = {
    0: {
            "path": Path('data/geojson/test'),
            "add_extension": None,
            "return_value": Path('data/geojson/test')
    },
    1: {
            "path": Path('data/geojson/test'),
            "add_extension": '.geojson',
            "return_value": Path('data/geojson/test.geojson')
    },
    2: {
            "path": Path('data/geojson/test.geojson'),
            "add_extension": '.kml',
            "return_value": Path('data/geojson/test.geojson.kml')
    }
}

path_to_file_path_parameters = {
    0: {
        "path": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson').as_posix(),
        "geolayer_name": 'test',
        "overwrite": True,
        "add_extension": None,
        "return_value": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test')
    },
    1: {
        "path": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test').as_posix(),
        "geolayer_name": 'test',
        "overwrite": True,
        "add_extension": None,
        "return_value": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test')
    },
    2: {
        "path": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test').as_posix(),
        "geolayer_name": 'test',
        "overwrite": True,
        "add_extension": '.geojson',
        "return_value": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test.geojson')
    },
    3: {
        "path": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson'),
        "geolayer_name": 'test',
        "overwrite": True,
        "add_extension": None,
        "return_value": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test')
    },
    4: {
        "path": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test'),
        "geolayer_name": 'test',
        "overwrite": True,
        "add_extension": None,
        "return_value": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test')
    },
    5: {
        "path": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test'),
        "geolayer_name": 'test',
        "overwrite": True,
        "add_extension": '.geojson',
        "return_value": Path(__file__).parent.parent.parent.parent.joinpath('data/geojson/test.geojson')
    }
}


def test_all():

    # add_extension_path
    print(test_function(add_extension_path, add_extension_path_parameters))

    # path_to_file_path
    print(test_function(path_to_file_path, path_to_file_path_parameters))


if __name__ == '__main__':
    test_all()
