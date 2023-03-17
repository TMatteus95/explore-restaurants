import streamlit as st
import pandas as pd 
import branca
import requests
import snowflake.connector
from urllib.error import URLError
import folium
from streamlit_folium import st_folium, folium_static

# Get data
restaurants = pd.DataFrame(columns = ['id', 'restaurant', 'url', 'newspaper', 'gps_lat', 'gps_long', 'color_marker'],
                           data = [[1,'HolySmoke BBQ', 'dn.se','Dagens Nyheter', 56.260860, 12.550790, 'red'],
                                   [2,'Vedens lustgård', 'gp.se','Göteborgs Posten',58.426000,13.464320, 'blue']])

restaurants_selected = st.sidebar.multiselect("Filter which restaurants you want to see the reviews of:", list(restaurants.iloc[:,3]), list(restaurants.iloc[:,3]))

restaurants_to_show = restaurants.loc[restaurants.loc[:,'newspaper'].isin(restaurants_selected)]


# Iitiate the map with a start location of gothenburg
m = folium.Map(location=[58.426000,13.464320], zoom_start=6)

# Adding a marker
tooltip = "Click me!"
for r in restaurants_to_show.itertuples(index=True, name='Pandas'):
  
  html="""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    h1 {
      color: blue;
      font-family: verdana;
      font-size: 300%;
    }
    p {
      color: red;
      font-family: courier;
      font-size: 160%;
    }
    </style>
    </head>
    <body>

    <h1>This is a heading</h1>
    <p>This is a paragraph.</p>

    </body>
    </html>
    """
  
  iframe = branca.element.IFrame(html=html, width=400, height=200)
  popup = folium.Popup(iframe, max_width=400)
  
  folium.Marker(
    location = [r.gps_lat, r.gps_long], 
    popup=popup, 
    tooltip=r.restaurant,
    icon=folium.Icon(color = r.color_marker, icon= None)
).add_to(m)

folium.TileLayer('cartodbdark_matter').add_to(m)

st_data = st_folium(m, width=700)


st.dataframe(restaurants_to_show)



