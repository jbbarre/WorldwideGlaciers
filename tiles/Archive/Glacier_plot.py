#NSIDC, April 2018.
#
# Sample program to read in a GeoTIFF file, extract the metadata,
# and create an image.
#
# The code has been tested with data from:
#    NSIDC-0725, MEaSUREs Greenland Ice Sheet Velocity Mosaics SAR and Landsat, Version 1
#      https://doi.org/10.5067/OBXCG75U7540
#    NSIDC-0478, MEaSUREs Greenland Ice Sheet Velocity Map InSAR Data, Version 2
#     https://doi.org/10.5067/OC7B04ZM9G6Q
#
# Note: Custom color map designed by Terry Haran, NSIDC.
#
# Required libraries:
#      numpy
#      rasterio
#      affine
#      matplotlib
#
# To use:
# Edit the file to change the GeoTIFF file name.
# Then run the code:
# python read_measures
#
import numpy as np
import rasterio
from affine import Affine
import matplotlib.pyplot as plt
import matplotlib.image as mping
import matplotlib.colors as colors

# directory path and file name
path = ''
file_in = 'Mosaic_HIMALAYA_BHUTAN_S2L8_2017-2018_2020September22_vo_AdaptFilter_3857.tif'

# read in file with geotiff geographic information
src = rasterio.open(path + file_in)

# print out metadata information
for k in src.meta:
  print(k,src.meta[k])

# Retrieve the affine transformation
if isinstance(src.transform, Affine):
     transform = src.transform
else:
     transform = src.affine

N = src.width
M = src.height
dx = transform.a
dy = transform.e
minx = transform.c
maxy = transform.f

# Read the image data, flip upside down if necessary
data_in = src.read(1)
if dy < 0:
  dy = -dy
  data_in = np.flip(data_in, 0)

print('Data minimum, maximum = ', np.amin(data_in), np.amax(data_in))

# Generate X and Y grid locations
xdata = minx + dx/2 + dx*np.arange(N)
ydata = maxy - dy/2 - dy*np.arange(M-1,-1,-1)

# Scale the velocities by the log of the data.
d = np.log(np.clip(data_in, 1, 3000))
data_scale = (255*(d - np.amin(d))/np.ptp(d)).astype(np.uint8)

# Construct an RGB table using a log scale between 1 and 3000 m/year.
vel = np.exp(np.linspace(np.log(1), np.log(3000), num=256))
hue = np.arange(256)/255.0
sat = np.clip(1./3 + vel/187.5, 0, 1)
value = np.zeros(256) + 0.75
hsv = np.stack((hue, sat, value), axis=1)
rgb = colors.hsv_to_rgb(hsv)
# Be sure the first color (the background) is white
rgb[0,:] = 1
cmap = colors.ListedColormap(rgb, name='velocity')

extent = [xdata[0], xdata[-1], ydata[0], ydata[-1]]
plt.figure(figsize=(8,8))
fig = plt.imshow(data_scale, extent=extent, origin='lower', cmap=cmap)
plt.title(file_in)
# Hide the axes and remove the space around them
plt.axis('off')
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)
tickval = [1, 10, 100, 1000, 3000]
t = np.log(tickval)
cb = plt.colorbar(fig, ticks=255*(t - t[0])/(t[-1] - t[0]), shrink=0.5)
cb.set_label('Velocity Magnitude (m/year)')
cb.ax.set_yticklabels(tickval)
plt.savefig("python_sample.png", dpi=300, bbox_inches='tight', pad_inches=0.5)
plt.show()