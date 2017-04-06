from shapely.geometry import mapping, Polygon
import fiona
import fiona.crs
import os
import pandas as pd

import cea.inputlocator
import cea.utilities.dbfreader as dbf


# The basic geometry
poly = Polygon([(0, 0), (8, 0), (8, 6), (0, 6)])

# The schema of the zone.shp shapefile
schema = {
    'geometry': 'Polygon',
    'properties': {'Name': 'str',
                   'floors_bg': 'int',
                   'floors_ag': 'int',
                   'height_bg': 'float',
                   'height_ag': 'float'},
}
crs = fiona.crs.from_string('+datum=WGS84 +k=1 +lat_0=39.76 +lon_0=-104.86 +no_defs +proj=tmerc +units=m +x_0=0 +y_0=0')

locator = cea.inputlocator.InputLocator(os.path.dirname(__file__))
locator._ensure_folder('inputs', 'building-geometry')


# Write the zone.shp shapefile
with fiona.open(locator.get_building_geometry(), 'w', driver='ESRI Shapefile', crs=crs, schema=schema) as c:
    # set latitude and longitude: latitude = 39.76, longitude = -104.86
    c.write({
        'geometry': mapping(poly),
        'properties': {'Name': 'B600',
                       'floors_bg': 0,
                       'floors_ag': 1,
                       'height_bg': 0.0,
                       'height_ag': 2.7},
        'crs': {'lat_0': 39.76, 'lon_0': -104.86}
    })

# Write the district.shp shapefile
with fiona.open(locator.get_district(), 'w', driver='ESRI Shapefile', crs=crs, schema=schema) as c:
    # set latitude and longitude: latitude = 39.76, longitude = -104.86
    c.write({
        'geometry': mapping(poly),
        'properties': {'Name': 'B600',
                       'floors_bg': 0,
                       'floors_ag': 1,
                       'height_bg': 0.0,
                       'height_ag': 2.7},
        'crs': {'lat_0': 39.76, 'lon_0': -104.86}
    })


# write the occupancy.dbf file
locator._ensure_folder('inputs', 'building-properties')

df = pd.DataFrame({
    'Name': ['B600'], 
    'PFloor': [0.0], 
    'OFFICE': [1.0]})
dbf.df2dbf(df, locator.get_building_occupancy())

# write the age.dbf file
df = pd.DataFrame({
    'Name': ['B600'],
    'built': [2017],
    'roof': [0],
    'windows': [0],
    'partitions': [0],
    'basement': [0],
    'HVAC': [0],
    'envelope': [0],})
dbf.df2dbf(df, locator.get_building_age())
