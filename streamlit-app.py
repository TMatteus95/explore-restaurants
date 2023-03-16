import streamlit as st
import pandas as pd 
import requests
import snowflake.connector
from urllib.error import URLError
import folium
from streamlit_folium import st_folium, folium_static

# Get data
restaurants = pd.DataFrame(columns = ['id', 'restaurant', 'url', 'newspaper', 'gps_lat', 'gps_long', 'color_marker'],
                           data = [[1,'HolySmoke BBQ', 'dn.se','Dagens Nyheter', 56.260860, 12.550790, 'red'],
                                   [2,'Vedens lustgård', 'gp.se','Göteborgs Posten',58.426000,13.464320, 'blue']])

restaurants_selected = st.multiselect("Filter which restaurants you want to see the reviews of:", list(restaurants.iloc[:,1]), list(restaurants.iloc[:,1]))

restaurants_to_show = restaurants.loc[restaurants.loc[:,'restaurant'].isin(restaurants_selected)]
st.dataframe(restaurants_to_show)

# Iitiate the map with a start location of gothenburg
m = folium.Map(location=[57.708870, 11.974560], zoom_start=6)

# Adding a marker
tooltip = "Click me!"
for r in restaurants_to_show.itertuples(index=True, name='Pandas'):
  folium.Marker(
    location = [r.gps_lat, r.gps_long], 
    popup="<p>Holy Smoke BBQ</p> <p>Recesent: Dagen nyheter  Betyg: 5/5 L&auml;nk: https://www.dn.se/kultur/holy-smoke-skansk-barbecue-pa-riktigt/</p>", 
    tooltip=tooltip,
    icon=folium.Icon(color = r.color_marker, icon= None)
).add_to(m)

folium.TileLayer('cartodbdark_matter').add_to(m)

st_data = st_folium(m, width=700)


# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
