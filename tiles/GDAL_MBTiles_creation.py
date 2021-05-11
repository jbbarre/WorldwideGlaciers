from osgeo import gdal
import os
from os import listdir
from os.path import isfile, join

# Change the working directory
os.chdir('D:\\3_DataViz\\2_glaciers\\1_data_himalaya\\data_3857\\')
mypath = os.getcwd()
out_folder = 'D:\\3_DataViz\\2_glaciers\\1_data_himalaya\\data_3857\\'
# Get the content of the folder
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

in_file='Mosaic_HIMALAYA_BHUTAN_S2L8_2017-2018_2020September22_vo_AdaptFilter_3857.tif'
out_file='Mosaic_HIMALAYA_BHUTAN_S2L8_2017-2018_2020September22_vo_AdaptFilter_3857.mbtiles'

# Create the mbtiles files
options = gdal.TranslateOptions( format = 'mbtiles')
#gdal.Translate(destName=out_file ,srcDS=in_file, options = options)

# Create the Zoom level [equivalent to gdaladdo with CLI]
Image = gdal.Open('Mosaic_HIMALAYA_BHUTAN_S2L8_2017-2018_2020September22_vo_AdaptFilter_3857.mbtiles', 1)  # 0 = read-only, 1 = read-write.
gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
Image.BuildOverviews('NEAREST', [4, 8, 16], gdal.TermProgress_nocb)
del Image  # close the dataset (Python object and pointers)

