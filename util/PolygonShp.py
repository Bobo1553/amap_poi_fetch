# coding=utf-8

import arcpy

input_shp_name = u'F:\\GeoData\\xian.shp'
city_name_field = "NAME"
city_name = u"朝阳区"


def get_boundary():
    arcpy.env.workspace = r'F:\GeoData'
    cursor = arcpy.da.SearchCursor('xian.shp',["SHAPE@", "NAME"])
    for row in cursor:
        if row[1] == city_name:
            extent = row[0].extent
            print([extent.XMin, extent.YMax, extent.XMax, extent.YMin])
            break
    pass


if __name__ == '__main__':
    get_boundary()
