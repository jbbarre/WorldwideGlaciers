# Raster Processing to produce MBtiles for Mapbox display

## 1. change the SRS from original (WGS84 UTM xx) to Web mercator (EPSG 3857)

  - Linux 
  ```console
    gdalwarp -t_srs EPSG:3857 Mosaic_HIMALAYA_BHUTAN_S2L8_2017-2018_2020September22_vo_AdaptFilter.tif data4326/bhutan.tif
  ```
 - Python -> see GDAL_reproject.py

 ## 2. Create MBtiles from tif files
Preparation: Depending on your input data, you may need to ‘expand’ your layer from a 1 band with colour table to a layer with 3 (RGB) or 4(RGBA) bands. This can be done with the gdal_translate function. You furthermore need to reproject your layer to Web Mercator projection (EPGS: 3857), which can be done with the gdalwarp function.
  ```console
      gdal_translate -expand rgba mymap1.tif mymap2.tif
      gdalwarp -t_srs EPSG:3857 -r near mymap2.tif mymap3.tif
  ```

Converting a raster layer to a MBtiles map takes two steps:
   - First, use ```gdal_translate``` to convert your raster layer to a tiles layer (see [here](https://gdal.org/drivers/raster/mbtiles.html) for MBtile specific options).This will only create the highest zoom level. Gdal_translate determines this automatically based on the image resolution.
   - Second, use the ```gdaladdo``` (https://gdal.org/programs/gdaladdo.html) function to build overview images, i.e., the lower zoom levels. Ex: ```gdaladdo -r nearest mymap.mbtiles 2 4 8 16```