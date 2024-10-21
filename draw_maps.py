import xarray as xr
import numpy as np
from glob import glob
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib as mpl
import os

if not os.path.exists('created-maps'):
    os.mkdir('created-maps')

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
    ax = plt.axes(projection=ccrs.Mercator())

    col1 = [0, 0, 0, 0]
    col2 = 'steelblue'
    newcmp = ListedColormap([col1, col2])
    ax.pcolormesh(lon, lat, mask, cmap=newcmp, transform=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, color=np.array((240, 240, 220)) / 256.)
    ax.add_feature(cfeature.COASTLINE)
    fileout = os.path.basename(f).replace('.nc', '.png')
    fileout = os.path.join('created-maps', fileout)
    plt.savefig(fileout, bbox_inches='tight')
    plt.close(fig)
