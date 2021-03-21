import streamlit as st
from streamlit_folium import folium_static
import folium

import config

tooltip = {{ tooltip|safe }}
location = {{ location|safe }}


m = folium.Map(
    location=location, zoom_start=16, 
    tiles=config.tiles['hst']['tiles'], 
    attr=config.tiles['hst']['name'],
)
folium.TileLayer(
    tiles=config.tiles['toa']['tiles'], 
    attr=config.tiles['toa']['name'],
).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)
folium.Marker(location, popup=tooltip, tooltip=tooltip).add_to(m)

folium_static(m)