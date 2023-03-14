import streamlit
import pandas as pd 
import requests
import snowflake.connector
from urllib.error import URLError
import folium
from streamlit_folium import st_folium, folium_static



m = folium.Map(location=[57.708870, 11.974560], zoom_start=6)

tooltip = "Click me!"

folium.Marker(
    [56.260860, 12.550790], popup="<p>Holy Smoke BBQ</p> <p>Recesent: Dagen nyheter  Betyg: 5/5 L&auml;nk: https://www.dn.se/kultur/holy-smoke-skansk-barbecue-pa-riktigt/</p>", tooltip=tooltip
).add_to(m)
folium.TileLayer('cartodbdark_matter').add_to(m)

st_data = st_folium(m, width=700)
