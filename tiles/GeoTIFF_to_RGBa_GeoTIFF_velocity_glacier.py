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
import matplotlib.colors as colors 
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import time
from datetime import timedelta


# Change the working directory
#os.chdir('D:\\3_DataViz\\2_glaciers\\1_data\\THICKNESS\\data_3857\\')
os.chdir('D:\\3_DataViz\\2_glaciers\\1_data\\VELOCITY\\data_3857\\done\\')
mypath = os.getcwd()

# Get the content of the folder
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#in_file='V_RGI-1.2_2021July01_3857.tif'
for in_file in onlyfiles :
    start_time = time.monotonic()
    # read GeoTIFF source
    src = gdal.Open(in_file, gdal.GA_ReadOnly) 

    # Note GetRasterBand() takes band no. starting from 1 not 0
    band = src.GetRasterBand(1)
    band.SetNoDataValue(0)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray()
    arr = np.nan_to_num(arr,posinf=-9999)
    #Create a masked array for making calculations without nodata values
    arr_ma = np.ma.masked_where(arr == -9999, arr, copy=True)

    #free memory
    arr = None
    del arr
    band = None
    del band

    # Scale the velocities by the log of the data.
    d = np.log(np.clip(arr_ma, 1, 500))
    # Rescaling (min-max normalization) - 255 for RGB ??
    scaled_ds = (255*(d - np.amin(d))/np.ptp(d)).astype(np.uint8)

    #free memory
    d = None
    del d


    # Build a custom colormap designed by Terry Haran, NSIDC, April 2018.
    # Build an RGB table using a log scale between 1 and 500 m/year.
    vel = np.exp(np.linspace(np.log(1), np.log(500), num=256)) 
    hue = np.arange(256) / 255.0 
    sat = np.clip(1. / 3 + vel / 187.5, 0, 1) 
    value = np.zeros(256) + 0.75 
    hsv = np.stack((hue, sat, value), axis=1) 
    rgb = colors.hsv_to_rgb(hsv) 
    # Be sure the first color (the background) is white
    rgb[0, :] = 1
    # Create the colormap 
    cmap = colors.ListedColormap(rgb, name='velocity')

    # ## From 1 band GeoTIFF to RGBa GeoTIFF
    # apply the colormap to the scaled data
    rgb_ds = cmap(scaled_ds)
    rgb_ds.shape

    #free memory
    scaled_ds = None
    del scaled_ds

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
    options = gdal.WarpOptions(format='GTiff', srcNodata=255, dstAlpha=True)
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

