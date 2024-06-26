import os
import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_folium import folium_static, st_folium
import folium
from shapely.geometry import Point
import plotly.graph_objects as go
import plotly.express as px
import random
# import duckdb

from handler import load_covid_data, load_geojson_data, filter_data, plot_gauge, filter_cases


#===============================================================================
#----------------------------------VISUALISASI----------------------------------
#===============================================================================

# # Streamlit app layout
st.set_page_config(page_title="Global COVID Monthly Data", page_icon=":bar_chart:", layout="wide")    
# # st.title("Monthly COVID-19 Data Dashboard")

# Sidebar filters
with st.sidebar:
    st.title('COVID 19 GLOBAL STATISTIC 2020-2022')
    year = st.selectbox("Year", [2020, 2021, 2022])
    month = st.selectbox("Month",['Entire Year'] + list(range(1, 13)))
    continent = st.selectbox("Continent", ["All Continent", "Asia", "Africa", "Europe", "North America", "South America", "Oceania", "Antarctica"])
    data_type = st.selectbox("Data Type", ["Total Confirmed Cases", "Total Recovered Cases", "Total Deaths"])

# map data_type yang dipiliah dengan kolom yang akan ditampilkan
column_mapping = {
    "Total Confirmed Cases": "total_confirmed",
    "Total Recovered Cases": "total_recovered",
    "Total Deaths": "total_deaths"
}

#========================================================================================
#----------------------------------PEMANGGILAN FUNCTION----------------------------------
#========================================================================================
# Load data
covid_df = load_covid_data()
geo_df, geojson_data = load_geojson_data()

# pemanggilan function filter_data
filtered_data = filter_data(covid_df, year, month, continent, column_mapping[data_type])
all_total_confirmed, all_total_recovered, all_total_death, total_cases = filter_cases(covid_df, year, month, continent)



#========================================================================================
#----------------------------------LAYOUT DASHBOARD--------------------------------------
#========================================================================================
top_left_col1, top_middle_col1, top_right_col1 = st.columns((2,0.2,2))
middle_left_col2, middle_right_col2 = st.columns((4,3))
bottom_left_col3, bottom_right_col3 = st.columns(2)

    
with top_left_col1:
    if all_total_confirmed and all_total_recovered and all_total_death and total_cases:
        
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                plot_gauge(total_cases, "cornflowerblue", "", "Total Cases", total_cases * 1.2)
            with col2:
                plot_gauge(all_total_confirmed, "yellow", "", "Total Confirmed", all_total_confirmed * 1.2)
            with col3:
                plot_gauge(all_total_recovered, "seagreen", "", "Total Recovered", all_total_recovered * 1.2)
            with col4:
                plot_gauge(all_total_death, "indianred", "", "Total Deaths", all_total_death * 1.2)
                
            # col1.metric("Total Cases", plot_gauge(total_cases, "darkblue", "", "Total Cases", total_cases * 1.2))
            # col2.metric("Total Confirmed", plot_gauge(all_total_confirmed, "darkblue", "", "Total Confirmed", all_total_confirmed * 1.2))
            # col3.metric("Total Recovered", plot_gauge(all_total_recovered, "darkblue", "", "Total Recovered", all_total_recovered * 1.2))
            # col4.metric("Total Deaths", plot_gauge(all_total_death, "darkblue", "", "Total Deaths", all_total_death * 1.2))
            
    else:
        st.warning("No data available for the selected filters.")

        
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Metric 5", "Value")
        col2.metric("Metric 6", "Value")
        col3.metric("Metric 7", "Value")
        col4.metric("Metric 8", "Value")
        col5.metric("Metric 9", "Value")

with top_right_col1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Metric 10", "Value")
    col2.metric("Metric 11", "Value")
    col3.metric("Metric 12", "Value")


with middle_left_col2:
    st.markdown(
        """
        <style>
        .map-container {
            height: 400px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    with st.container():
        # Initialize map
        # membuat Folium map
        m_type_1 = 'cartodbdark_matter'
        m_type_2 = 'cartodbpositron'
        m_type_3 = 'OpenStreetMap'

        m = folium.Map(location=[20, 0], zoom_start=2, tiles=m_type_1)
        
        # Add geojson data to map
        folium.Choropleth(
            geo_data=geojson_data,
            name='choropleth',
            data=filtered_data,
            columns=['country/region', column_mapping[data_type]],
            key_on='feature.properties.name',
            fill_color='GnBu',
            fill_opacity=0.5,
            line_opacity=0.2,
            legend_name=f'{data_type}',
        ).add_to(m)
        # COLOR PALLTTE https://colorbrewer2.org/#type=sequential&scheme=GnBu&n=3
        
        folium_static(m, width=550, height=300)

with middle_right_col2:
    st.write("Middle right column content")


with bottom_left_col3:
    st.write("Bottom left column content")

with bottom_right_col3:
    st.write("Bottom right column content")