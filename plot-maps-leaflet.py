import folium
import xarray as xr
import numpy as np
import matplotlib as mp
import os
import matplotlib.colors as cl
from pathlib import Path
from domains import domains

cmap = mp.colormaps['Spectral']

# Function to reconstruct the IFrame HTML from text and
# style
def build_html(text):
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
    strout += text
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
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
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

tile1.add_to(m)

cpt = 0
N = len(domains) - 1
for d in domains.values():
    if N == 0:
        color = cmap(0)
    else:
        color = cmap(cpt / N)
    color = cl.to_hex(color, keep_alpha=False)
    lonbnd = d['lonbnd']
    latbnd = d['latbnd']
    lon = [lonbnd[0], lonbnd[1], lonbnd[1], lonbnd[0], lonbnd[0]]
    lat = [latbnd[0], latbnd[0], latbnd[1], latbnd[1], latbnd[0]]
    points = np.array([lat, lon]).T + cpt * 10

    with open(d['popup'], 'r') as f:
        content = f.read()
    iframe = folium.IFrame(build_html(content))
    popup = folium.Popup(iframe,
                     min_width=500,
                     max_width=500)

    folium.Polygon(
        locations=points,
        weight=1,
        color=color,
        fill_color=color,
        fill_opacity=0.5,
        fill=True,
        popup=popup,
        #tooltip="Click me!",
    ).add_to(m)

    cpt += 1


m.save('index.html')
