#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 08:30:40 2022

Module Compilation : Craig Ramseyer, Used With Permission

Coding done by: NATALIE OLESON, ADALIA TRUONG
"""

#BRINING IN THE GOODS
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs 
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter

from geocat.viz import util as gvutil 
from geocat.viz import cmaps as gvcmaps


#DATA COMING IN AND READING
file = "hackydata.nc"
folder = "/home/craig/Documents/"
filename = folder+file

ds= xr.open_dataset(filename, decode_times = True)

#TIME STEP 17 
ts = 17


 
#CONVERTING INTO CORRECT UNITS
t_prec = ds.tp.values*1000
[a,b,c] = np.where(t_prec==np.amax(t_prec))
mslp = ds.msl.isel(time=ts).drop('time')/100
t = ds.tp.isel(time=ts).drop('time')*1000
mslp = ds.msl.isel(time=ts).drop('time')/100



t_lev = np.arange(0,35,2) #PRECIPT INTERVALS
mslp_lev = np.arange(800 ,1100,6)



#MAP TIME
cmap = 'inferno'
plt.figure(figsize = (10,8))
ax = plt.axes(projection= ccrs.PlateCarree())

ax.set_extent([np.min(ds.longitude), 
               np.max(ds.longitude), 
               np.min(ds.latitude), 
               np.max(ds.latitude)], 
              crs=ccrs.PlateCarree())

ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor = 'white', facecolor = 'none')




states_provinces = cfeature.NaturalEarthFeature(category = 'cultural', 
                                               name = "admin_1_states_provinces_lines",
                                               scale = "50m", 
                                               facecolor = 'None')

temp = t.plot.contourf(ax = ax, 
                       transform = ccrs.PlateCarree(), 
                       cmap = cmap, 
                       levels = t_lev, 
                       extend = 'both',
                       add_colorbar= False,
                       add_labels = "False")

plt.colorbar(temp,ax=ax,ticks=t_lev, orientation = "horizontal", pad = 0.075)
mslp_plot = mslp.plot.contour(ax=ax, 
                              transform = ccrs.PlateCarree(),
                              levels = mslp_lev,
                              colors="cyan",
                              linewidths = 2,
                              add_labels = True)


ax.add_feature(states_provinces, edgecolor = 'white', zorder = 2) 


ax.clabel(mslp_plot,fmt = '%d', levels = mslp_lev) 

[
 txt.set_bbox(dict(facecolor= 'none', edgecolor = 'none', pad = 1))
  for txt in mslp_plot.labelTexts
]

gvutil.set_titles_and_labels(ax, maintitle= "Sea Level Pressure/Precipt for Hurricane Isabella")

gvutil.add_lat_lon_ticklabels(ax)
ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=""))
ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=""))

gvutil.add_major_minor_ticks(ax, x_minor_per_major = 3, y_minor_per_major= 5, labelsize= 12)






out_folder = '/home/craig/Documents/'
plot_out_str = 'hurr_isabel_precip_'
plt.savefig(out_folder+plot_out_str+'.png',dpi=1500)


plt.show()

