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

with open('html/title.html', 'r') as fout:
    title_html = fout.read()

cmap = mp.colormaps['hsv']

# Function to reconstruct the IFrame HTML from text and
# style
def build_html(dom):
    print(dom)
    dom_name = dom[0]
    dom_val = dom[1]
    file_html = os.path.join('html', dom_name + '.html')
    print("------------------- ", file_html)
    if os.path.isfile(file_html):
        with open(file_html, 'r') as f:
            text = f.read()
    else:
        text = ''
    #print(text)

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

    print(d)
    f = dom_val['map'].replace('.nc', '.png')
    fileout = os.path.basename(f).replace('.nc', '.png')
    fileout = os.path.join('created-maps', fileout)
    # print(fileout)

    data_uri = base64.b64encode(open(fileout, 'rb').read()).decode('utf-8')
    strout += '<div align="center">\n'
    img_tag = '<img src="data:image/png;base64,{0}" height="200" align="center">'.format(data_uri)
    strout += img_tag + '\n'
    strout += '</div>'
    strout += text

    file_csv = f'csv/{dom_name}.csv'
    if os.path.isfile(file_csv):
        # print("Write config in table")
        conf = pd.read_csv(file_csv, sep=',', header=None)
        conf = conf.fillna('')
        html = conf.to_html(header=False, index=False)
        html = html.replace('class="dataframe"', 'class="table-striped w-auto"')
        strout += '<div align="center">\n'
        strout += html
        strout += '</div>'

    strout += """
    </body>
</html>
"""

    return strout

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
for dom in domains.items():
    key = dom[0]
    d = dom[1]
    print(key, d)

    # print('---------------------------------- ', d['title'])
    iframe = branca.element.IFrame(build_html(dom), width=500, height=800)
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


    status = 'prod'
    icon_color = 'darkblue'
    color = 'lightgray'
    if 'status' in d.keys():
        status = d['status']
    if status == 'dev':
        icon_color = 'darkred'

    factor = 0.5
    lonmin = float(data['lon'].min())
    lonmax = float(data['lon'].max())
    latmin = float(data['lat'].min()) + lat_offset
    latmax = float(data['lat'].max()) + lat_offset
    image = data['mask'].values[::-1, :]

    folium.Marker(
            location=[data['lat'].mean(), data['lon'].mean()],
            popup=popup, icon=folium.Icon(prefix='fa', icon='fish', color=color, icon_color=icon_color)).add_to(m)

    cpt += 1

m.get_root().html.add_child(folium.Element(title_html))

m.save('build/index.html')
