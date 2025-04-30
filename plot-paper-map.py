# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from glob import glob
import numpy as np
import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import os

# +
projin = ccrs.PlateCarree()

filelist = glob('maps/*nc')
filelist.remove('maps/zyork_mask.nc')
filelist.append('maps/zyork_mask.nc')
#filelist.remove('maps/grid_baltic.nc')
filelist.remove('maps/gom_mask.nc')
filelist.append('maps/gom_mask.nc')
filelist.remove('maps/jiaozhou_bay.nc')
filelist.append('maps/jiaozhou_bay.nc')
filelist.remove('maps/cooperation-sea-mask.nc')
filelist.append('maps/cooperation-sea-mask.nc')
filelist


# -

def get_bounds(lon, lat):
    lontmp = np.array([lon.min(), lon.max(), lon.max(), lon.min(), lon.min()])
    lattmp = np.array([lat.min(), lat.min(), lat.max(), lat.max(), lat.min()])
    return lontmp, lattmp


# +
fig = plt.figure(figsize=(18, 12))
plt.subplots_adjust(wspace=0.2, hspace=0.2, left=0.6, bottom=0.6)

offset = 0.1
projout = ccrs.InterruptedGoodeHomolosine()
ax = plt.axes([offset, offset,1 - 2*offset, 1-2*offset], projection=projout) # left, bottom, width, height
ax.add_feature(cfeature.LAND)
filelist


# -

def get_bounds(lon, lat):
    lontmp = np.array([lon.min(), lon.max(), lon.max(), lon.min(), lon.min()])
    lattmp = np.array([lat.min(), lat.min(), lat.max(), lat.max(), lat.min()])
    return lontmp, lattmp


# +
fig = plt.figure(figsize=(18, 12))
plt.subplots_adjust(wspace=0.2, hspace=0.2, left=0.6, bottom=0.6)

offset = 0.1
projout = ccrs.InterruptedGoodeHomolosine()
ax = plt.axes([offset, offset,1 - 2*offset, 1-2*offset], projection=projout) # left, bottom, width, height
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.OCEAN)
ax.set_global()
ax.stock_img()

# plt.rcParams['image.cmap'] = 'RdBu'

colors = []

for f in filelist:
    print(f)
    # Processing canada
    data = xr.open_dataset(f)
    lon = data['lon'].values
    lat = data['lat'].values
    mask = data['mask'].values
    mask = np.ma.masked_where(mask == 0, mask)
    lontmp, lattmp = get_bounds(lon, lat)
    ll = ax.plot(lontmp, lattmp, transform=ccrs.PlateCarree(), lw=3)
    colors.append(ll[0].get_color())
plt.savefig('figure-osmose-paper.jpeg', dpi=1000)

i = 0
for f in filelist[:]:
    data = xr.open_dataset(f)
    mask = data['mask']
    if 'lon_b' in data.variables:
        lon = data['lon_b']
        lat = data['lat_b']
    else:
        lon = data['lon']
        lat = data['lat']

    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.Mercator())

    col1 = [0, 0, 0, 0]
    col2 = 'steelblue'
    newcmp = ListedColormap([col1, col2])
    ax.pcolormesh(lon, lat, mask, cmap=newcmp, transform=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, color=np.array((240, 240, 220)) / 256.)
    ax.add_feature(cfeature.COASTLINE, lw=2)
    
    for spine in ax.spines.values():
        spine.set_edgecolor(colors[i])
        spine.set_linewidth(4)
    i += 1
    
    fileout = os.path.basename(f).replace('.nc', '.png')
    #fileout = os.path.join('/home/BARRIER/Nextcloud/Synchronisation', fileout)
    plt.savefig(fileout, bbox_inches='tight', dpi=500)
    plt.close(fig)
# -


