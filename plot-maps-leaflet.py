import folium
import xarray as xr
import numpy as np
import matplotlib as mp
import os
import matplotlib.colors as cl
from pathlib import Path
from domains import domains
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import branca
import base64

cmap = mp.colormaps['hsv']

# Function to reconstruct the IFrame HTML from text and
# style
def build_html(d):
    
    with open(d['popup'], 'r') as f:
        text = f.read()
    
    strout = ""
    strout += """
<!DOCTYPE html>
<html>
    <head>
        <style>
    """
    strout += style
    strout += """
        </style>
    </head>
    <body>
    """
    
    toto = d['map'].replace('.nc', '.png')
    data_uri = base64.b64encode(open(toto, 'rb').read()).decode('utf-8')
    strout += '<div align="center">\n'
    img_tag = '<img src="data:image/png;base64,{0}" height="200" align="center">'.format(data_uri)
    strout += img_tag + '\n'
    strout += '</div>'
    strout += text
    strout += """
    </body>
</html>
"""

    return strout

def colorize(array, r, g, b):

    array = array.astype(int)
    col1 = [r, g, b, 0]
    col2 = [r, g, b, 1]
    newcmp = ListedColormap([col1, col2])
    normed_data = (array - array.min()) / (array.max() - array.min())

    fig = plt.figure()
    cs = plt.imshow(array, cmap=newcmp)
    cs.set_clim(0, 1)
    plt.colorbar(cs)
    plt.savefig(str(cpt))
    plt.close(fig)
    
    return newcmp(normed_data)

# Recover the content of the HTML file
import pathlib
with open('style.css', 'r') as f:
    style = f.read()

# Create a Map instance
m = folium.Map(zoom_start=3, control_scale=True, location=[0, 0], tiles=None)

tile1 = folium.TileLayer(
    #tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite',
    overlay=False,
    control=True
)

tile2 = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
        attr = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
        overlay=False,
        control=True
        )

tile3 = folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',
    attr = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
    overlay=False,
    control=True
)

tile1.add_to(m)

BASE_COLORS = {'k': (0.0, 0.0, 0.0), 'g': (0, 0.5, 0), 'r': (1, 0, 0), 'c': (0, 0.75, 0.75), 'm': (0.75, 0, 0.75), 'y': (0.75, 0.75, 0)}
#BASE_COLORS = {}
#BASE_COLORS['blue'] = (12.2 / 100, 46.7 / 100, 70.6 / 100)
#BASE_COLORS['orange'] = (100 / 100, 49.8 / 100, 5.5 / 100)

colnames = list(BASE_COLORS.keys())

# +
cpt = 0
N = len(domains) - 1
for d in domains.values():
    print('---------------------------------- ', d['title'])
    r, g, b = BASE_COLORS[colnames[cpt % len(colnames)]]

    iframe = branca.element.IFrame(build_html(d), width=500, height=800)
    popup = folium.Popup(iframe,
                     min_width=500,
                     max_width=500, min_height=800)

    data = xr.open_dataset(d['map'])
    if(data['lon'].values.ndim == 1):
        dlon = np.mean(np.diff(data['lon'].values))
        dlat = np.mean(np.diff(data['lat'].values))
    else:
        dlon = np.mean(np.diff(data['lon'].values[0, :]))
        dlat = np.mean(np.diff(data['lat'].values[:, 0]))

    if 'lat_offset' in d.keys():
        lat_offset = d['lat_offset']
    else:
        lat_offset = 0

    factor = 0.5
    lonmin = float(data['lon'].min())
    lonmax = float(data['lon'].max())
    latmin = float(data['lat'].min()) + lat_offset
    latmax = float(data['lat'].max()) + lat_offset
    image = data['mask'].values[::-1, :]
    display = colorize(image, r, g, b)

    folium.Marker(
            location=[data['lat'].mean(), data['lon'].mean()],
            popup=popup).add_to(m)

    #folium.raster_layers.ImageOverlay(
    #    display,
    #    bounds=[[latmin, lonmin], [latmax, lonmax]],
    #).add_to(m)


    #folium.Rectangle(
    #    bounds=[[latmin, lonmin], [latmax, lonmax]],
    #    weight=0,
    #    color=(r, g, b),
    #    fill_color=(r, g,b),
    #    fill_opacity=0.0,
    #    fill=True,
    #    popup=popup,
    #    tooltip=d['title'],
    #    line_join="round",
    #).add_to(m)

    cpt += 1

m.save('index.html')
# -
