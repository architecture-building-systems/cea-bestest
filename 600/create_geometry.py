from shapely.geometry import mapping, Polygon
import fiona
import os
import cea.inputlocator

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

locator = cea.inputlocator.InputLocator(os.path.dirname(__file__))
locator._ensure_folder('inputs', 'building-geometry')

# Write the zone.shp shapefile
with fiona.open(locator.get_building_geometry(), 'w', 'ESRI Shapefile', schema) as c:
    c.write({
        'geometry': mapping(poly),
        'properties': {'Name': 'B600',
                       'floors_bg': 0,
                       'floors_ag': 1,
                       'height_bg': 0.0,
                       'height_ag': 2.7},
    })

