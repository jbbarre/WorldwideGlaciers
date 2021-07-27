from osgeo import gdal
import os
from os import listdir
from os.path import isfile, join

# Change the working directory
#os.chdir('D:\\3_DataViz\\2_glaciers\\1_data\\VELOCITY\\data_3857\\')
os.chdir('D:\\3_DataViz\\2_glaciers\\1_data\\THICKNESS\\data_3857\\')
mypath = os.getcwd()

# Get the content of the folder
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#in_file='Velocity_RGI-1_2_comp.tif'
in_file='THICKNESS_RGI-17.7_2021July23_3857_rgba_comp.tif'
#for in_file in onlyfiles :

out_file= in_file.replace('_rgba_comp.tif','.mbtiles')

# Create the mbtiles files
creation_opt = ["TILE_FORMAT=PNG8"]
options = gdal.TranslateOptions(format = 'mbtiles')
gdal.Translate(destName=out_file ,srcDS=in_file, options = options,creationOptions= creation_opt)

# Create the Zoom level [equivalent to gdaladdo with CLI]
Image = gdal.Open(out_file, 1)  # 0 = read-only, 1 = read-write.
gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
Image.BuildOverviews('GAUSS', [2, 4, 8, 16, 32], gdal.TermProgress_nocb)
del Image  # close the dataset (Python object and pointers)