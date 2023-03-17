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
    <div style='background-color: rgba(255, 255, 255, 0.5); border-radius: 5px;'>
        <h3>San Francisco</h3>
        <p>Welcome to San Francisco! This is a beautiful city located in the heart of the Bay Area.</p>
    </div>
    """
  
  iframe = branca.element.IFrame(html=html, width=400, height=200)
  popup = folium.Popup(html, max_width=400, opacity = 0)
  
  folium.Marker(
    location = [r.gps_lat, r.gps_long], 
    popup=popup, 
    tooltip=r.restaurant,
    opacity= 1, 
    icon=folium.Icon(color = r.color_marker, icon= None)
).add_to(m)
  marker._icon.style['background'] = 'rgba(0, 0, 0, 0.0)'
  marker._icon.style['border-radius'] = '10px'
  marker._icon.style['border'] = 'none'
  marker._shadow.style['display'] = 'none'

folium.TileLayer('cartodbdark_matter').add_to(m)



st_data = st_folium(m, width=700)


st.dataframe(restaurants_to_show)



