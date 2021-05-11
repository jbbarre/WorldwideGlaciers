# Methode de mosaiquage des raster tuilés

## 1. Génération d'un VRT départemental pour QGIS

  - Linux (testé mais non utilisé car l'utilisateur postgres n'a pas les droits dans infogeo)
  ```console
    gdalbuildvrt /tmp/dep_001.vrt ./OHR_RVB_0M20_JP2-E080_LAMB93_D01-2018/*.jp2 -overwrite -a_srs EPSG:2154 -addalpha
  ```

  - Windows             
  ```console
    "C:/OSGeo4W64/bin/gdalbuildvrt.exe" "\\data2\infogeo\ign\BD_ORTHO_HR\OHR_RVB_0M20_JP2-E080_LAMB93_D01-2018\ASSEMBLAGE\dep_01.vrt" "\\data2\infogeo\ign\BD_ORTHO_HR\OHR_RVB_0M20_JP2-E080_LAMB93_D01-2018\*.jp2" -overwrite -a_srs EPSG:2154 -addalpha
  ```

## 2. Calcul des statistiques du VRT pour accélérer l'ouverture sur QGIS

  - Linux
  ```console
    gdalinfo -approx_stats /tmp/dep_001.vrt
  ```

  - Windows
  ```console   
    "C:/OSGeo4W64/bin/gdalinfo.exe" -approx_stats "\\data2\infogeo\ign\BD_ORTHO_HR\OHR_RVB_0M20_JP2-E080_LAMB93_D01-2018\ASSEMBLAGE\dep_01.vrt"
  ```

## 3. Construction d'une pyramide d'images pour les utilisateurs qui ouvrent le vrt avec un zoom départemental

  - Windows
  ```console
    "C:/OSGeo4W64/bin/gdaladdo.exe" -ro --config COMPRESS_OVERVIEW LZW --config INTERLEAVE_OVERVIEW PIXEL "\\data2\infogeo\ign\BD_ORTHO_HR\OHR_RVB_0M20_JP2-E080_LAMB93_D01-2018\ASSEMBLAGE\dep_01.vrt" 32
  ```

## 4. Génération de la dalle départementale en JP2000 à partir du VRT (non realisé)
  ```console
    "C:/OSGeo4W64/bin/gdal_translate.exe" -of JP2OpenJPEG -co QUALITY=8 \\data2\infogeo\ign\BD_ORTHO_HR\OHR_RVB_0M20_JP2-E080_LAMB93_D01-2018\ASSEMBLAGE\dep_01.vrt"  "\\data2\infogeo\ign\BD_ORTHO_HR\OHR_RVB_0M20_JP2-E080_LAMB93_D01-2018\dep_01.jp2"
  ```

## Ces commandes ont été intégrées dans le script scap_ign_irc.R afin d'automatiser la génération des VRT pour BD_ORTHO_HR et BD_SCAN25_TOPO
