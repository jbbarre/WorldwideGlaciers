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

```gdalbuildvrt thickness_rgi-1.vrt *.tif```

```gdalbuildvrt -input_file_list list.txt V_rgi-1-9.vrt```

```gdal_translate -of mbtiles thickness_rgi-1.vrt thickness_rgi-1.mbtiles```
```gdal_translate -of mbtiles V_rgi-1-9.vrt V_rgi-1-9.mbtiles```

 ```gdaladdo -r nearest thickness_rgi-1.mbtiles  2 4 8 16```

 ## 3. Create MBtiles from shp files

Merge shp files into one shp file:

```ogrmerge.py -single -o  glacier_outlines.shp *.shp```

Convert the shp file into geojson:

```ogr2ogr -f "GeoJSON" glacier_outlines.json "glacier_outlines.shp"```


Convert GeoJSON to Mbtiles:

```tippecanoe -zg -o glacier_outlines.mbtiles --drop-densest-as-needed --extend-zooms-if-still-dropping -s EPSG:4326 --force  glacier_outlines_all.json  ```

## 4.a reproject Antarctica

From 3031 to 4326

```gdalwarp -overwrite -s_srs EPSG:3031 -t_srs EPSG:4326 -te -180 -90 180 90 Antarctica_2020-07-15_v02_thickness.tif Antarctica_2020-07-15_v02_thickness_4326.tif```
gdalwarp -overwrite -s_srs EPSG:3412 -t_srs EPSG:4326 -te -180 -90 180 90 antarctica_velocity.tif antarctica_velocity.tif_4326.tif

## 4.b reproject Greenland

From 3413 to 3857

```gdalwarp -s_srs epsg:3413 -t_srs epsg:3857 .\greenland_velocity.tif .\greenland_velocity_3857.tif```

## 5. Geotiff processing

### Merge Geotiff files 
```dir  *.tif > list.txt```

```gdalwarp -multi --optfile list.txt Velocity_RGI-2.tif```


### Compression & GEOTIFF

https://gist.github.com/kgjenkins/877ff0bf7aef20f87895a6e93d61fb43

https://gis.stackexchange.com/questions/1104/should-gdal-be-set-to-produce-geotiff-files-with-compression-which-algorithm-sh

https://kokoalberti.com/articles/geotiff-compression-optimization-guide/


pour créer un fichier TIFF avec une compression en JPEG pour servir for image serving, using open source rendering engines :

```gdal_translate  -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR dest.tif src.tif```

sans perte de données
```gdal_translate -co compress=lzw -co predictor=2 src_dataset dst_dataset```


For those using newer GDAL versions, there's also the lossless ZStandard (ZSTD) compression (GDAL>=2.3) and lossy Limited Error Raster Compression (LERC) compression (GDAL>=2.4) choices available.

Generally speaking though, ZSTD offers faster data read speeds than both LZW and DEFLATE with similar compression ratios, though it can be somewhat slower when writing the file (depending on what settings you use).

If you're not that fussed about data precision (e.g. only doing visualization rather than analysis), then LERC might be a good option. There is a MAX_Z_ERROR setting that allows you to tweak how much precision you are willing to sacrifice. E.g. a MAX_Z_ERROR=0.001 or 1mm gave a space saving of 50% in one benchmark (see ref).

The best part is that you can also combine LERC with ZSTD using COMPRESS=LERC_ZSTD! Or if you prefer using DEFLATE, you can do COMPRESS=LERC_DEFLATE. See also full list of combinations/settings at the official GDAL GeoTIFF docs https://gdal.org/drivers/raster/gtiff.html#creation-options

More details and full benchmark comparisons can be found at this valuable reference:

'Guide to GeoTIFF compression and optimization with GDAL' by @kokoalberti