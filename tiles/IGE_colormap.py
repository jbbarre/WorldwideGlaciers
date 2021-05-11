import numpy as np 
from osgeo import gdal,ogr 
import matplotlib.colors as colors 

#Construction d'un relief ombragé à partir d'un MNT 
#shaded=np.roll(dem,-6)-dem 
#shaded=sc.medfilt2d(np.float32(shaded),5) 
#w=np.where(shaded>200) 
#shaded[w]=200 
#w=np.where(shaded<-200) 
#shaded[w]=-200 
#im=np.copy(shaded) 

#Clipping avec les vitesses 
#val = (np.float32(im)-np.nanmin(im)) / (np.nanmax(im)-np.nanmin(im)) 
#val = val**0.7 
#ind = (v == 0) 
#v[v > 500]=500 
#v[v < 5]=5 
#h = np.log10(v) 
#h = h / np.nanmax(h) 
#h[ind]=0. 
#s = (0.5+v/125.0)/1.5 
#s[s > 1] =1 
#s[ind]=0. 
#size=v.shape 
#hsv = np.zeros([size[0],size[1],3]) 
#hsv[:,:,0]=h 
#hsv[:,:,1]=s 
#hsv[:,:,2]=val 
#velrgb = matplotlib.colors.hsv_to_rgb(hsv) 
#velrgb[dem<14]=255 

# Construct a colormap with log scale 
# designed by Terry Haran, NSIDC, April 2018. 
vel = np.exp(np.linspace(np.log(5), np.log(500), num=256)) 
hue = np.arange(256) / 255.0 
sat = np.clip(1. / 3 + vel / 187.5, 0, 1) 
value = np.zeros(256) + 0.75 
hsv = np.stack((hue, sat, value), axis=1) 
rgb = colors.hsv_to_rgb(hsv) 
rgb[0, :] = 1 
rgb = np.round(rgb*100,0)
cmap = colors.ListedColormap(rgb, name='velocity')
# fmt='%i' : format to obtain integer notation without 00000
np.savetxt('colormap.txt',rgb, fmt='%d',delimiter=' ')

# create linear velocity range from 1 to 500
#speed = np.arange(1,1500,5.859375)
#rgb = np.column_stack((speed,rgb))

#np.savetxt('D:\\3_DataViz\\2_glaciers\\1_data_himalaya\\glacier_colormap.txt',rgb,fmt='%d',delimiter=' ')

