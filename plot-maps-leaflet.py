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
import pandas as pd

if not os.path.exists('build'):
    os.mkdir('build')


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
    """
    strout += boostrap_link
    strout += "\n"

    strout +=  """
        <style>
    """
    strout += style

    strout += """
        </style>
    </head>
    <body>
    """

    f = d['map'].replace('.nc', '.png')
    fileout = os.path.basename(f).replace('.nc', '.png')
    fileout = os.path.join('created-maps', fileout)
    # print(fileout)

    data_uri = base64.b64encode(open(fileout, 'rb').read()).decode('utf-8')
    strout += '<div align="center">\n'
    img_tag = '<img src="data:image/png;base64,{0}" height="200" align="center">'.format(data_uri)
    strout += img_tag + '\n'
    strout += '</div>'
    strout += text

    if 'config' in d.keys():
        # print("Write config in table")
        conf = pd.read_csv(d['config'], sep=',', header=None)
        conf = conf.fillna('')
        html = conf.to_html(header=False, index=False)
        html = html.replace('class="dataframe"', 'class="table-striped table-hover w-auto"')
        strout += '<div align="center">\n'
        strout += html
        strout += '</div>'

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

boostrap_link = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">'


# +
cpt = 0
N = len(domains) - 1
for d in domains.values():
    # print('---------------------------------- ', d['title'])
    if list(domains.keys())[cpt] == 'NS':
        lala = 2
        print(build_html(d))
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

    folium.Marker(
            location=[data['lat'].mean(), data['lon'].mean()],
            popup=popup, icon=folium.Icon(prefix='fa', icon='fish', color='darkblue', icon_color='white')).add_to(m)

    cpt += 1

m.save('build/index.html')
