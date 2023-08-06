from tests.data.geolayers import (
    geolayer_attributes_only,
    geolayer_attributes_only_boolean_false,
    geolayer_geometry_only_all_geometries_type,
    geolayer_fr_dept_data_and_geometry,
    geolayer_attributes_to_force_only_forced
)

from geoformat_lib.driver.geoformat_to_postgresql import geolayer_to_postgres

host = "localhost"
database_name = "tcdev"
user = "tc"
password = "tc1234"
port = 5432
schema = "guilhain"
geometry_column_name = "geom"
overwrite = True

geolayer_to_postgres(
    geolayer=geolayer_attributes_only,
    host=host,
    database_name=database_name,
    user=user,
    password=password,
    port=port,
    schema=schema,
    geometry_column_name='geom',
    overwrite=True,
    constraint_geometry_type=False,
    consider_width_and_precision=True
)


geolayer_to_postgres(
    geolayer=geolayer_geometry_only_all_geometries_type,
    host=host,
    database_name=database_name,
    user=user,
    password=password,
    port=port,
    schema=schema,
    geometry_column_name='geom',
    overwrite=True,
    constraint_geometry_type='Polygon',
    consider_width_and_precision=True
)

geolayer_to_postgres(
    geolayer=geolayer_fr_dept_data_and_geometry,
    host=host,
    database_name=database_name,
    user=user,
    password=password,
    port=port,
    schema=schema,
    geometry_column_name='geom',
    overwrite=True,
    constraint_geometry_type=False,
    consider_width_and_precision=True
)

geolayer_to_postgres(
    geolayer=geolayer_attributes_to_force_only_forced,
    host=host,
    database_name=database_name,
    user=user,
    password=password,
    port=port,
    schema=schema,
    geometry_column_name='geom',
    overwrite=True,
    constraint_geometry_type=False,
    consider_width_and_precision=True
)

geolayer_to_postgres(
    geolayer=geolayer_attributes_only_boolean_false,
    host=host,
    database_name=database_name,
    user=user,
    password=password,
    port=port,
    schema=schema,
    geometry_column_name='geom',
    overwrite=True,
    constraint_geometry_type=False,
    consider_width_and_precision=True
)
