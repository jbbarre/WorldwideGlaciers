from osgeo import gdal, osr
import os
import io
import numpy as np

def array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array,format,spatialRef):

    bands = array.shape[0]
    cols = array.shape[1]
    rows = array.shape[2]

    originX = rasterOrigin[0]
    originY = rasterOrigin[1]

    driver = gdal.GetDriverByName(format)
    outRaster = driver.Create(newRasterfn, cols, rows, bands,gdal.GDT_UInt16,options = ['PHOTOMETRIC=RGB', 'PROFILE=GeoTIFF',])
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))

    for band in range(bands):
        outRaster.GetRasterBand(band+1).WriteArray(array[band,:,:])
        outRaster.GetRasterBand(band+1).FlushCache()
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(spatialRef)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())


def get_rgb_bands():
    source = gdal.Open("C:\\RGBtest.tif")

    red = source.GetRasterBand(1).ReadAsArray()
    green = source.GetRasterBand(2).ReadAsArray()
    blue = source.GetRasterBand(3).ReadAsArray()

    #rgbOutput = source.ReadAsArray() #Easier method
    rgbOutput = np.zeros((3,16,16), 'uint16')

    rgbOutput[0,...] = red
    rgbOutput[1,...] = green
    rgbOutput[2,...] = blue

    #Clear so file isn't locked
    source = None
    return rgbOutput

exampleRGB = get_rgb_bands()

exampleOutput = "C:\\ExampleOutput.tif"
rasterOrigin=[0,0]

array2raster(exampleOutput,rasterOrigin,1, 1,exampleRGB,'GTiff',3879) 

createdFile = gdal.Open("C:\\ExampleOutput.tif")

print 'old file info:'+gdal.Info(source)
print 'new file info:'+gdal.Info(createdFile)

createdFile = None

exampleOutput = None