import xarray as xr
import numpy as np
from glob import glob
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib as mpl

filelist = glob('maps/*nc')

for f in filelist:
    data = xr.open_dataset(f)
    mask = data['mask']
    if 'lon_b' in data.variables:
        lon = data['lon_b']
        lat = data['lat_b']
    else:
        lon = data['lon']
        lat = data['lat']

    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())

    col1 = [0, 0, 0, 0]
    col2 = 'steelblue'
    newcmp = ListedColormap([col1, col2])
    ax.pcolormesh(lon, lat, mask, cmap=newcmp, transform=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, color='DarkGray', zorder=3)
    ax.add_feature(cfeature.COASTLINE, zorder=4)
    plt.savefig(f.replace('.nc', '.svg'), bbox_inches='tight')
    plt.close(fig)
