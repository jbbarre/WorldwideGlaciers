# ## Display and Create RGBa GeoTIFF
#  - Create the colormap
#  - Get the RGB band from this colormap
#  - Create a 3 bands (RGB geotiff) from the 1band GeoTIFF 
# 
# Worldwide Glaciers project - IGE - JB Barré - 11/05/2021

from osgeo import gdal,osr
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import cmocean
import time
from datetime import timedelta


# Change the working directory
os.chdir('D:\\3_DataViz\\2_glaciers\\1_data\\THICKNESS\\data_3857\\')
mypath = os.getcwd()

# Get the content of the folder
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#in_file='THICKNESS_RGI-1.1_2021July01_3857.tif'
for in_file in onlyfiles :
    start_time = time.monotonic()
    # read GeoTIFF source
    src = gdal.Open(in_file, gdal.GA_ReadOnly) 

    # Note GetRasterBand() takes band no. starting from 1 not 0
    band = src.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray()
    arr [arr == 0] =-9999
    #Create a masked array for making calculations without nodata values
    arr = np.ma.masked_equal(arr, -9999)

    ## From 1 band GeoTIFF to RGBa GeoTIFF
    # Normalization du np.array between [0 to 1]
    norm_arr =  arr - arr.min() 
    norm_arr /= arr.max()-arr.min()
    # Apply the colormap to dataset
    cmap=cmocean.cm.ice_r
    rgb_ds = cmap(norm_arr)
    norm_arr = None
    del norm_arr
    # Scale RGB values from [0,1] to [0,255]
    data_array_scaled = np.interp(rgb_ds,(0, 1), (0, 255))
    # Round to the nearest bigger integer
    data_array_scaled = np.ceil(data_array_scaled)
    data_array_scaled = data_array_scaled.astype(int)

    # rescale RGB values from [0,1] to [0,255]
    data_array_scaled = np.interp(rgb_ds,(0, 1), (0, 255))
    #free memory
    rgb_ds = None
    del rgb_ds 

    # Creates a copy of a 3-band raster with values from array'''
    # GeoTIFF creation options : https://gdal.org/drivers/raster/gtiff.html

    # Destination file name 
    rgb_file = in_file.replace('.tif','_rgb.tif')

    # info from source
    geotransform = src.GetGeoTransform ()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    bands = data_array_scaled.shape[2]-1
    rows = src.RasterXSize
    cols = src.RasterYSize

    # Get geotiff driver
    driver = gdal.GetDriverByName('GTiff')
    options = ['PHOTOMETRIC=RGB', 'PROFILE=GeoTIFF','COMPRESS=LZW','PREDICTOR=2']

    # Create new raster
    dest = driver.Create(rgb_file,rows,cols, bands, eType=gdal.GDT_Byte,options=options)
    dest.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))

    # Set metadata.SetGeoTransform(src.GetGeoTransform())
    dest.GetRasterBand(1).WriteArray(np.around(data_array_scaled[:,:,0]))
    dest.GetRasterBand(1).SetNoDataValue(255)
    dest.GetRasterBand(2).WriteArray(np.around(data_array_scaled[:,:,1]))
    dest.GetRasterBand(2).SetNoDataValue(255)
    dest.GetRasterBand(3).WriteArray(np.around(data_array_scaled[:,:,2]))
    dest.GetRasterBand(3).SetNoDataValue(255)

    destSRS = osr.SpatialReference()
    destSRS.ImportFromEPSG(3857)
    dest.SetProjection(destSRS.ExportToWkt())

    # Close dataset
    data_array_scaled= None
    del data_array_scaled
    dest = None
    del dest

    # add an alpha band to the RGB for transparent background in Mapbox
    rgba_file =rgb_file.replace('rgb','rgba')
    rgba_comp_file =rgba_file.replace('.tif','_comp.tif')

    #create alpha band
    options = gdal.WarpOptions(format='GTiff', srcNodata=0, dstAlpha=True)
    dest = gdal.Warp(rgba_file, rgb_file, options=options)
    dest = None

    #compress GTiff
    ds = gdal.Open(rgba_file)
    tr_options = gdal.TranslateOptions(creationOptions = ['COMPRESS=LZW','PREDICTOR=2'])
    ds = gdal.Translate(rgba_comp_file, ds,options=tr_options)
    ds = None

    #delete uncompress rgba_file
    os.remove(rgba_file)
    os.remove(rgb_file)

    #processing time 
    end_time = time.monotonic()
    print(rgba_comp_file, "| Fichier traité en ",timedelta(seconds=end_time - start_time)," s.")






