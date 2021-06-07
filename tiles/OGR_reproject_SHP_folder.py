# Reprojection of SHP file
# from https://pcjericks.github.io/py-gdalogr-cookbook/projection.html
# 
# 27/05/2021

from osgeo import ogr
from osgeo import osr
import os
from os import listdir
from os.path import isfile, join

#change the working directory
in_path = 'D:\\3_DataViz\\2_glaciers\\2_shp\\rawdata\\'
out_path = 'D:\\3_DataViz\\2_glaciers\\2_shp\\'
# get the content of the folder
onlyfiles = [f for f in listdir(in_path) if isfile(join(in_path, f)) if os.path.splitext(in_path+f)[1]=='.shp']

for in_file in onlyfiles :
    # get the input layer
    driver = ogr.GetDriverByName('ESRI Shapefile')
    #ine_file = r'D:/3_DataViz/2_glaciers/2_shp/RGI_ALASKA_EASTERN_2_Millanetal_v06May2021.shp'
    inDataSet = driver.Open(in_path+in_file)
    inLayer = inDataSet.GetLayer()

    # input SpatialReference from Layer
    spatialRef = inLayer.GetSpatialRef()
    in_crs = int(spatialRef.GetAttrValue("PROJCS|AUTHORITY", 1))
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(in_crs)

    # output SpatialReference
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(3857)

    # create the CoordinateTransformation
    coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

    # create the output layer
    outputShapefile = in_file.replace('.shp','_3857.shp')
    if os.path.exists(outputShapefile):
        driver.DeleteDataSource(outputShapefile)
    outDataSet = driver.CreateDataSource(out_path+outputShapefile)
    outLayer = outDataSet.CreateLayer(in_file.replace('.shp','_3857'),outSpatialRef, geom_type=ogr.wkbMultiPolygon)

    # add fields
    inLayerDefn = inLayer.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        outLayer.CreateField(fieldDefn)

    # get the output layer's feature definition
    outLayerDefn = outLayer.GetLayerDefn()

    # loop through the input features
    inFeature = inLayer.GetNextFeature()
    while inFeature:
        # get the input geometry
        geom = inFeature.GetGeometryRef()
        # reproject the geometry
        geom.Transform(coordTrans)
        # create a new feature
        outFeature = ogr.Feature(outLayerDefn)
        # set the geometry and attribute
        outFeature.SetGeometry(geom)
        for i in range(0, outLayerDefn.GetFieldCount()):
            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
        # add the feature to the shapefile
        outLayer.CreateFeature(outFeature)
        # dereference the features and get the next input feature
        outFeature = None
        inFeature = inLayer.GetNextFeature()
    print('file reprojected: '+outputShapefile)

    # Save and close the shapefiles
    inDataSet = None
    outDataSet = None

