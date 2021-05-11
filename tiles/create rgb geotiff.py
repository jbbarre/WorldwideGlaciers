from osgeo import gdal
import os
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import matplotlib.colors as colors 
import numpy as np



# Change the working directory
os.chdir('D:\\3_DataViz\\2_glaciers\\1_data_himalaya\\data_3857\\')
mypath = os.getcwd()
out_folder = 'D:\\3_DataViz\\2_glaciers\\1_data_himalaya\\data_3857\\'
# Get the content of the folder
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

in_file='Mosaic_HIMALAYA_BHUTAN_S2L8_2017-2018_2020September22_vo_AdaptFilter_3857.tif'

# Construct a colormap with log scale 
# designed by Terry Haran, NSIDC, April 2018. 
vel = np.exp(np.linspace(np.log(5), np.log(1500), num=256)) 
hue = np.arange(256) / 255.0 
sat = np.clip(1. / 3 + vel / 187.5, 0, 1) 
value = np.zeros(256) + 0.75 
hsv = np.stack((hue, sat, value), axis=1) 
rgb = colors.hsv_to_rgb(hsv) 
rgb[0, :] = 1 
cmap = colors.ListedColormap(rgb, name='velocity')

dataset = gdal.Open(in_file, gdal.GA_ReadOnly) 
# Note GetRasterBand() takes band no. starting from 1 not 0
band = dataset.GetRasterBand(1)
arr = band.ReadAsArray()

#rgb_arr = cmap(arr[0,0])
rgb_func = lambda t : cmap(t)
rgb_arr = np.array([rgb_func(xi) for xi in arr])
#R band
#R_band = rgb_arr[:,:,0]
#G band
#G_band = rgb_arr[:,:,1]
#B band
#B_band = rgb_arr[:,:,2]
#alpha band
#A_band = rgb_arr[:,:,3]


def createRGB(template,arr,filename):
    '''Creates a copy of a 3-band raster with values from array

    Arguments:

        template: Path to template raster
        arr: Value array with dimensions (r,c,3)
        filename: Output filename for new raster 
    '''

    # Open template
    t = gdal.Open(template)

    # Get geotiff driver
    driver = gdal.GetDriverByName('GTiff')

    # Create new raster
    r = driver.Create(filename, t.RasterXSize, t.RasterYSize, 3, gdal.GDT_Byte,['COMPRESS=LZW'])

    # Set metadata
    r.SetGeoTransform(t.GetGeoTransform())
    r.SetProjection(t.GetProjection())

    # loop through bands and write new values
    for bix in range(3):
        rb = r.GetRasterBand(bix+1)
        # Write array
        rb.WriteArray(arr[:,:,bix])

    # Close datasets
    t = None
    r = None
    rb = None

#createRGB('D:\\3_DataViz\\2_glaciers\\1_data_himalaya\\data_3857\\Mosaic_HIMALAYA_BHUTAN_S2L8_2017-2018_2020September22_vo_AdaptFilter_3857.tif',rgb_arr,'rgb_tif.tif')


import rasterio
from rasterio.plot import show

fp = 'D:\\3_DataViz\\2_glaciers\\1_data_himalaya\\data_3857\\rgb_tif.tif'
#img = rasterio.open(fp)
#show(img)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

imgplot = plt.imshow(rgb_arr)
plt.show()