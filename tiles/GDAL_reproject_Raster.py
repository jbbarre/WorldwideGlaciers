from osgeo import gdal
import os
from os import listdir
from os.path import isfile, join

#change the working directory
os.chdir('D:\\3_DataViz\\2_glaciers\\1_data_himalaya')
mypath = os.getcwd()
out_folder = 'D:\\3_DataViz\\2_glaciers\\1_data_himalaya\\data_3857\\'
# get the content of the folder
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in onlyfiles :
    ds = gdal.Open(i)
    out_file = i.replace('.tif','_3857.tif')
    warp_options = gdal.WarpOptions(dstSRS = 'EPSG:3857')
    gdal.Warp(destNameOrDestDS = out_folder+out_file, srcDSOrSrcDSTab = ds, options = warp_options)
    print("Processing done for "+out_file)

