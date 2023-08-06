from pathlib import Path

from geoformat_lib.driver.geojson_driver import (
    geojson_to_geolayer,
    geolayer_to_geojson
)

from tests.data.geolayers import (
    geolayer_geometry_only_all_geometries_type,
    geolayer_attributes_only_without_none_value,
    geolayer_fr_dept_population,
    geolayer_fr_dept_geometry_only,
    geolayer_fr_dept_data_only
)
from tests.test_all import test_function

from tests.geoformat_lib.driver.ogr.compare_ogr_files import compare_geolayer


def geojson_driver():
    
    file_path_base = Path(__file__).parent.parent.parent.parent.joinpath
    ###########################################################################
    #
    # TEST BASICS GEOMETRY AND DATA
    #
    ###########################################################################
    # test geometries
    all_geometries_path = file_path_base('tests/geoformat_lib/driver/test/all_geometry_type_only.geojson')
    geolayer_to_geojson(
        geolayer=geolayer_geometry_only_all_geometries_type,
        path=all_geometries_path,
        overwrite=True,
        add_extension=True
    )
    geolayer_geometry_only_all_geometries_type_2 = geojson_to_geolayer(
        path=all_geometries_path,
        field_name_filter=None,
        geometry_type_filter=None,
        bbox_extent=False,
        bbox_filter=None,
        serialize=False,
        feature_limit=None,
        feature_offset=None,
        force_field_conversion=False,
        crs=4326
    )

    # geolayer with geometry only
    geometry_only_path = file_path_base('tests/geoformat_lib/driver/test/FRANCE_DPT_GENERALIZE_LAMB93_ROUND_GEOMETRY_ONLY.geojson')
    geolayer_to_geojson(
        geolayer=geolayer_fr_dept_geometry_only,
        path=geometry_only_path,
        overwrite=True,
        add_extension=True
    )

    geolayer_fr_dept_geometry_only_2 = geojson_to_geolayer(
        path=geometry_only_path,
        field_name_filter=None,
        geometry_type_filter=None,
        bbox_extent=True,
        bbox_filter=None,
        serialize=False,
        feature_limit=None,
        feature_offset=None,
        force_field_conversion=False,
        crs=2154
    )

    # test data
    geolayer_attributes_only_path = file_path_base('tests/geoformat_lib/driver/test/attributes_only.geojson')
    geolayer_to_geojson(
        geolayer=geolayer_attributes_only_without_none_value,
        path=geolayer_attributes_only_path,
        overwrite=True,
        add_extension=True
    )
    geolayer_attributes_only_without_none_value_2 = geojson_to_geolayer(
        path=geolayer_attributes_only_path,
        field_name_filter=None,
        geometry_type_filter=None,
        bbox_extent=False,
        bbox_filter=None,
        serialize=False,
        feature_limit=None,
        feature_offset=None,
        force_field_conversion=True,
        crs=None
    )

    # geolayer with data only
    geolayer_fr_dept_data_only_geojson_path = file_path_base('tests/geoformat_lib/driver/test/FRANCE_DPT_GENERALIZE_LAMB93_ROUND_DATA_ONLY.geojson')
    geolayer_to_geojson(
        geolayer=geolayer_fr_dept_data_only,
        path=geolayer_fr_dept_data_only_geojson_path,
        overwrite=True,
        add_extension=True
    )
    geolayer_fr_dept_data_only_2 = geojson_to_geolayer(
        path=geolayer_fr_dept_data_only_geojson_path,
        field_name_filter=None,
        geometry_type_filter=None,
        bbox_extent=True,
        bbox_filter=None,
        serialize=False,
        feature_limit=None,
        feature_offset=None,
        force_field_conversion=False,
        crs=None
    )

    # geolayer with data only 2
    data_only_path = file_path_base('tests/geoformat_lib/driver/test/dept_population.geojson')
    geolayer_to_geojson(
        geolayer=geolayer_fr_dept_population,
        path=data_only_path,
        overwrite=True,
        add_extension=True
    )
    geolayer_fr_dept_population_2 = geojson_to_geolayer(
        path=data_only_path,
        field_name_filter=None,
        geometry_type_filter=None,
        bbox_extent=False,
        bbox_filter=None,
        serialize=False,
        feature_limit=None,
        feature_offset=None,
        force_field_conversion=False,
        crs=None
    )

    return \
        geolayer_geometry_only_all_geometries_type == geolayer_geometry_only_all_geometries_type_2 \
            and \
        geolayer_fr_dept_geometry_only == geolayer_fr_dept_geometry_only_2 \
            and \
        geolayer_attributes_only_without_none_value == geolayer_attributes_only_without_none_value_2 \
            and \
        geolayer_fr_dept_data_only == geolayer_fr_dept_data_only_2 \
            and \
        geolayer_fr_dept_population == geolayer_fr_dept_population_2


test_geojson_parameters = {
    0: {
        "return_value": True
    }
}


def test_all():

    # geojson
    print(test_function(geojson_driver, test_geojson_parameters))


if __name__ == '__main__':
    test_all()


