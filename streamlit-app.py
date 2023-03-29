import streamlit as st
import pandas as pd 
import branca
import requests
import snowflake.connector
from urllib.error import URLError
import folium
from streamlit_folium import st_folium, folium_static
import datetime as dt
from dateutil.relativedelta import relativedelta # to add days or years


# Get data
restaurants = pd.DataFrame(columns = ['id', 'restaurant', 'url', 'newspaper', 'gps_lat', 'gps_long', 'color_marker'],
                           data = [[1,'HolySmoke BBQ', 'https://www.dn.se','Dagens Nyheter', 56.260860, 12.550790, 'red'],
                                   [2,'Vedens lustgård', 'https://www.gp.se','Göteborgs Posten',58.426000,13.464320, 'blue']])

###
### Create sidebar 
###

## Select newspaper
restaurants_selected = st.sidebar.multiselect("Jag vill se recensioner från följande tidningar:", list(restaurants.iloc[:,3]), list(restaurants.iloc[:,3]))
# filter data according to selection
restaurants_to_show = restaurants.loc[restaurants.loc[:,'newspaper'].isin(restaurants_selected)]

## Select date
format = 'MMM DD, YYYY'  # format output
start_date = dt.date(year=2021,month=1,day=1)-relativedelta(years=2)  #  I need some range in the past
end_date = dt.datetime.now().date()-relativedelta(years=2)
max_days = end_date-start_date

slider = st.sidebar.slider('Select date', min_value=start_date, value=(start_date, end_date) ,max_value=end_date, format=format)
## Sanity check
st.table(pd.DataFrame([[start_date, slider, end_date]],
              columns=['start',
                       'selected',
                       'end'],
              index=['date']))


# Initiate the map with a start location of gothenburg
m = folium.Map(location=[58.426000,13.464320], zoom_start=6)

# Adding a marker
for r in restaurants_to_show.itertuples(index=True, name='Pandas'):
  
  html="""
    <div style='background-color: white; border-radius: 5px;'>
        <h3>{}</h3>
        <p>Jag kan läsa mer om recensionen på {}: <a href="{}" target="_blank" >{}</a></p>
    </div>
    """.format(r.restaurant, r.newspaper, r.url, ".".join(r.url.split(".")[1:]))
  
  iframe = branca.element.IFrame(html=html, width=150, height=200)
  popup = folium.Popup(html, max_width=150)
  
  # We can add ->     tooltip=r.restaurant
  # for restuarant name when hover over marker
  marker = folium.Marker(
    location = [r.gps_lat, r.gps_long], 
    popup=popup, 
    icon=folium.Icon(color = r.color_marker, icon= None)
)

  marker.add_to(m)

folium.TileLayer('cartodbdark_matter').add_to(m)

st_data = st_folium(m, width=700)


st.dataframe(restaurants_to_show)



