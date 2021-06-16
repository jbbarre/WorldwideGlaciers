from osgeo import gdal
import os
from os import listdir
from os.path import isfile, join

# Change the working directory
os.chdir('D:\\3_DataViz\\2_glaciers\\0_Greenland\\')
mypath = os.getcwd()

# Get the content of the folder
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

in_file='greenland_vel_mosaic250_v0_v1_3857_rgba.tiff'
#in_file='buthan.vrt'
out_file='greenland_vel_mosaic250_v0_v1_3857_rgba.mbtiles'

# Create the mbtiles files
creation_opt = ["TILE_FORMAT=PNG8"]
options = gdal.TranslateOptions(format = 'mbtiles')
gdal.Translate(destName=out_file ,srcDS=in_file, options = options,creationOptions= creation_opt)

# Create the Zoom level [equivalent to gdaladdo with CLI]
Image = gdal.Open('greenland_vel_mosaic250_v0_v1_3857_rgba.mbtiles', 1)  # 0 = read-only, 1 = read-write.
gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
Image.BuildOverviews('GAUSS', [2, 4, 8, 16, 32], gdal.TermProgress_nocb)
del Image  # close the dataset (Python object and pointers)