import copy
import types
import warnings


def test_dependencies():

    try:
        from osgeo import ogr
        from osgeo import osr
        import_ogr_success = True
    except ImportError:
        import_ogr_success = False

    try:
        import psycopg2
        import psycopg2.extras
        import_psycopg2_success = True
    except ImportError:
        import_psycopg2_success = False

    return {'ogr': import_ogr_success, 'osr': import_psycopg2_success, 'psycopg2': import_psycopg2_success}

def print_errors(in_error):
    if in_error:
        sentence = ''
        for error in in_error:
            (id_parameters, error_message, returned_values) = error
            sentence += "\tThe parameters #{} returned errors: \n".format(id_parameters)
            sentence += "\t\t" + error_message + '\n'
            sentence += "\t\t" + returned_values + '\n'
        return sentence
    else:
        return False


def test_function(function, test_parameters):

    in_error = []
    test_parameters_copy = copy.deepcopy(test_parameters)
    for id_parameters, parameters in test_parameters_copy.items():
        return_value = parameters['return_value']
        del parameters['return_value']
        result_value = function(**parameters)

        # if return is a generator we transform it to tuple
        if isinstance(result_value,  types.GeneratorType):
            result_value = tuple(result_value)

        if result_value != return_value:
            in_error.append(
                (id_parameters,
                 'ERROR: return value must be {return_value}'.format(return_value=return_value),
                 'ERROR: function return this {result_value}'.format(result_value=result_value)))

    error_value = print_errors(in_error)
    if error_value:
        sentence = '{function_name} KO\n'.format(function_name=function.__name__)
        sentence += error_value
        warnings.warn(sentence)
    else:
        sentence = '{function_name} OK'.format(function_name=function.__name__)

    return sentence


def test_all():

    import tests.geoformat_lib.conf.test_format_variable
    import tests.geoformat_lib.conversion.test_bbox_conversion
    import tests.geoformat_lib.conversion.test_coordinates_conversion
    import tests.geoformat_lib.conversion.test_feature_conversion
    import tests.geoformat_lib.conversion.test_fields_conversion
    import tests.geoformat_lib.conversion.test_geolayer_conversion
    import tests.geoformat_lib.conversion.test_geometry_conversion
    import tests.geoformat_lib.conversion.test_metadata_conversion
    import tests.geoformat_lib.conversion.test_precision_tolerance_conversion
    import tests.geoformat_lib.conversion.test_segment_conversion
    import tests.geoformat_lib.driver.test_geojson_driver
    import tests.geoformat_lib.explore_data.test_print_data
    import tests.geoformat_lib.geoprocessing.connectors.test_operations
    import tests.geoformat_lib.geoprocessing.connectors.test_predicates
    import tests.geoformat_lib.geoprocessing.geoparameters.test_bbox
    import tests.geoformat_lib.geoprocessing.geoparameters.test_boundaries
    import tests.geoformat_lib.geoprocessing.geoparameters.test_lines
    import tests.geoformat_lib.geoprocessing.matrix.test_adjacency
    import tests.geoformat_lib.geoprocessing.measure.test_area
    import tests.geoformat_lib.geoprocessing.measure.test_distance
    import tests.geoformat_lib.geoprocessing.measure.test_length
    import tests.geoformat_lib.geoprocessing.test_area
    import tests.geoformat_lib.geoprocessing.test_merge_geometries
    import tests.geoformat_lib.geoprocessing.test_length
    import tests.geoformat_lib.geoprocessing.test_line_merge
    import tests.geoformat_lib.geoprocessing.test_split
    import tests.geoformat_lib.index.attributes.test_hash
    import tests.geoformat_lib.index.geometry.test_grid
    import tests.geoformat_lib.processing.data.test_field_statistics

    tests.geoformat_lib.conf.test_format_variable.test_all()
    tests.geoformat_lib.conversion.test_bbox_conversion.test_all()
    tests.geoformat_lib.conversion.test_coordinates_conversion.test_all()
    tests.geoformat_lib.conversion.test_feature_conversion.test_all()
    tests.geoformat_lib.conversion.test_fields_conversion.test_all()
    tests.geoformat_lib.conversion.test_geolayer_conversion.test_all()
    tests.geoformat_lib.conversion.test_geometry_conversion.test_all()
    tests.geoformat_lib.conversion.test_metadata_conversion.test_all()
    tests.geoformat_lib.conversion.test_precision_tolerance_conversion.test_all()
    tests.geoformat_lib.conversion.test_segment_conversion.test_all()
    tests.geoformat_lib.driver.test_geojson_driver.test_all()
    tests.geoformat_lib.explore_data.test_print_data.test_all()
    tests.geoformat_lib.geoprocessing.connectors.test_operations.test_all()
    tests.geoformat_lib.geoprocessing.connectors.test_predicates.test_all()
    tests.geoformat_lib.geoprocessing.geoparameters.test_bbox.test_all()
    tests.geoformat_lib.geoprocessing.geoparameters.test_boundaries.test_all()
    tests.geoformat_lib.geoprocessing.geoparameters.test_lines.test_all()
    tests.geoformat_lib.geoprocessing.matrix.test_adjacency.test_all()
    tests.geoformat_lib.geoprocessing.measure.test_area.test_all()
    tests.geoformat_lib.geoprocessing.measure.test_distance.test_all()
    tests.geoformat_lib.geoprocessing.measure.test_length.test_all()
    tests.geoformat_lib.geoprocessing.test_area.test_all()
    tests.geoformat_lib.geoprocessing.test_merge_geometries.test_all()
    tests.geoformat_lib.geoprocessing.test_length.test_all()
    tests.geoformat_lib.geoprocessing.test_line_merge.test_all()
    tests.geoformat_lib.geoprocessing.test_split.test_all()
    tests.geoformat_lib.index.attributes.test_hash.test_all()
    tests.geoformat_lib.index.geometry.test_grid.test_all()
    tests.geoformat_lib.processing.data.test_field_statistics.test_all()

if __name__ == '__main__':
    test_all()
