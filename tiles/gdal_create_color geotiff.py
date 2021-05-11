import numpy as np
import os
from osgeo import osr, gdal

data_array = np.load('fini.tif.npy')
data_array = data_array[::-1]
data_array_scaled = np.interp(data_array, (data_array.min(), data_array.max()), (0, 255))
data_array_scaled[data_array_scaled == 156.91450597804007] = -9999

r = data_array_scaled

RES    = 0.025
WIDTH  = data_array_scaled.shape[1]
HEIGHT = data_array_scaled.shape[0]

output_file = "out.tif"

# Create GeoTIFF
driver = gdal.GetDriverByName("GTiff")
dst_ds = driver.Create(output_file, WIDTH, HEIGHT, 1, gdal.GDT_Byte)

# Upper Left x, Eeast-West px resolution, rotation, Upper Left y, rotation, North-South px resolution
dst_ds.SetGeoTransform( [ -180, 0.025, 0, 90, 0, -0.025 ] )

# Set CRS
srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection( srs.ExportToWkt() )

# Write the band
dst_ds.GetRasterBand(1).SetNoDataValue(-9999) #optional if no-data transparent
dst_ds.GetRasterBand(1).WriteArray(r)


band = dst_ds.GetRasterBand(1)
colors = gdal.ColorTable()

colors.SetColorEntry(1, (112, 153, 89))
colors.SetColorEntry(2, (242, 238, 162))
colors.SetColorEntry(3, (242, 206, 133))
colors.SetColorEntry(4, (194, 140, 124))
colors.SetColorEntry(5, (214, 193, 156))

band.SetRasterColorTable(colors)
band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
del band, dst_ds

colors = gdal.ColorTable()
colors.CreateColorRamp(0, (229, 245, 249), 127, (153, 216, 201))
colors.CreateColorRamp(127, (153, 216, 201), 254, (44, 162, 95))
band.SetRasterColorTable(colors)
band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)

#CreateColorRamp(self, *args)
#CreateColorRamp(ColorTable self, int nStartIndex, ColorEntry startcolor, int nEndIndex, ColorEntry endcolor)