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
import altair as alt
import plotly.express as px
# import duckdb

from handler import load_covid_data, load_geojson_data, filter_data, plot_gauge, filter_cases, top_n_countries, display_top_countries, calculate_new, plot_metric, display_covid_dataframe, load_all_covid_data, filter_by_jenis_day, plot_donut_chart, plot_bar


#===============================================================================
#----------------------------------VISUALISASI----------------------------------
#===============================================================================

# # Streamlit app layout
# st.set_page_config(page_title="Global COVID Monthly Data", page_icon=":bar_chart:", layout="wide")    
# # st.title("Monthly COVID-19 Data Dashboard")

st.set_page_config(
    page_title="Covid-19 Global Statistic Dashboard",
    # page_icon="🏂",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Sidebar filters
with st.sidebar:
    # st.title('COVID 19 GLOBAL STATISTIC 2020-2022')
    st.markdown('# COVID 19 GLOBAL STATISTIC 2020-2022')
    year = st.selectbox("Year", [2020, 2021, 2022])
    month = st.selectbox("Month",['Entire Year'] + list(range(1, 13)))
    continent = st.selectbox("Continent", ["All Continent", "Asia", "Africa", "Europe", "North America", "South America", "Oceania", "Antarctica"])
    # st.write("\n")
    # data_type = st.radio("Map Data Type", ["Confirmed", "Recovered", "Deaths"])
    # data_type = st.selectbox("Map Data Type", ["Confirmed Cases", "Recovered Cases", "Deaths"])

# map data_type yang dipiliah dengan kolom yang akan ditampilkan
column_mapping = {
    "Confirmed": "total_confirmed",
    "Recovered": "total_recovered",
    "Deaths": "total_deaths"
}

# month_mapping = {
#     'Entire Year':'Entire Year',
#     1: "January",
#     2: "February", 
#     3: "March", 
#     4: "April", 
#     5: "May", 
#     6: "June",
#     7: "July", 
#     8: "August", 
#     9: "September", 
#     10: "October", 
#     11: "November", 
#     12: "December"
# }

#========================================================================================
#----------------------------------PEMANGGILAN FUNCTION----------------------------------
#========================================================================================
# Load data
covid_df = load_covid_data()
all_covid_df = load_all_covid_data()
geo_df, geojson_data = load_geojson_data()
all_total_confirmed, all_total_recovered, all_total_death, total_cases = filter_cases(covid_df, year, month, continent)
new_cases, new_confirmed, new_deaths, recovery_percentage, mortality_percentage = calculate_new(covid_df, year, month, continent)



#========================================================================================
#----------------------------------LAYOUT DASHBOARD--------------------------------------
#========================================================================================
top_left_col1, top_right_col1 = st.columns((4,3), gap="medium")
# top_left_col1, top_middle_col, top_right_col1 = st.columns((2,0.3,2),)
middle_left_col2, middle_right_col2 = st.columns((4,3), gap="medium")
bottom_left_col3, bottom_right_col3 = st.columns((5,3), gap="medium")

with middle_left_col2:
    # data_type = st.selectbox("", ["Confirmed Cases", "Recovered Cases", "Deaths Cases"])
    st.markdown("#### World Map Distribution of COVID-19")
    data_type = st.radio("Map Data Type", ["Confirmed", "Recovered", "Deaths"], horizontal=True)
    filtered_data = filter_data(covid_df, year, month, continent, column_mapping[data_type])
    with st.container():
        # Initialize map
        # membuat Folium map
        m_type_1 = 'cartodbdark_matter'
        m_type_2 = 'cartodbpositron'
        m_type_3 = 'OpenStreetMap'

        m = folium.Map(location=[20, 0], zoom_start=2, tiles=m_type_1)
        
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

        folium.GeoJson(
            geojson_data,
            style_function=lambda feature: {
                'fillColor': 'transparent',
                'color': 'black',
                'weight': 0.7,
                'fillOpacity': 0,
            },
            highlight_function=lambda feature: {
                'fillColor': 'white',
                'color': 'white',
                'weight': 2,
                'fillOpacity': 0.5,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['name'],
                aliases=['Country:'],
                style=("background-color: white; color: black; font-weight: bold;")
            )
        ).add_to(m)
        
        folium_static(m, width=550, height=300)

with middle_right_col2:
    st.markdown("#### Distribution of Covid-19 by Country")
    display_covid_dataframe(covid_df, year, month, continent)
    # display_covid_df = display_covid_dataframe(covid_df, year, month, continent)
    # st.dataframe(display_covid_df, use_container_width=True)
    

with top_left_col1:
    if all_total_confirmed or all_total_recovered or all_total_death or total_cases:
        st.write("\n")
        with st.container():
            col1, col2, col3, col4 = st.columns((4), gap="medium")
            with col1:
                plot_gauge(total_cases, "cornflowerblue", "", "Total Cases", total_cases)
            with col2:
                plot_gauge(all_total_confirmed, "yellow", "", "Total Confirmed", total_cases)
            with col3:
                plot_gauge(all_total_recovered, "seagreen", "", "Total Recovered", total_cases)
            with col4:
                    plot_gauge(all_total_death, "indianred", "", "Total Deaths", total_cases)
    else:
        st.warning("No data available for the selected filters.")

        
    with st.container():
        # col1, col2, col3, col4, col5 = st.columns((5), gap="medium")
        # col1, col2, col3, col4 = st.columns((4), gap="medium")
        col1, col2, col3 = st.columns((3), gap="medium")
        with col1:
            # st.markdown("###### New Cases")
            plot_metric(
                "New Cases",
                new_cases,
                prefix="",
                suffix="",
                show_graph=True,
                color_graph="rgba(0, 104, 201, 0.2)",
            )
        with col2:
            # st.markdown("##### New Cases")
            plot_metric(
                "New Confirm",
                new_confirmed,
                prefix="",
                suffix="",
                show_graph=True,
                color_graph="rgba(255, 255, 0, 0.2)",
            )
        with col3:
            # st.markdown("##### New Cases")
            plot_metric(
                "New Deaths",
                new_deaths,
                prefix="",
                suffix="",
                show_graph=True,
                color_graph="rgba(255, 43, 43, 0.2)",
            )

    with st.container():
        # # col1, col2, col3, col4, col5 = st.columns((5), gap="medium")
        # # col1, col2, col3, col4 = st.columns((4), gap="medium")
        col1, col2 = st.columns((2), gap="medium")
        with col1:
            # st.markdown("##### New Cases")
            plot_metric(
                "Recovery %",
                recovery_percentage,
                prefix="",
                suffix="%",
                show_graph=True,
                color_graph="rgba(0, 128, 0, 0.2)",
            )
        with col2:
            # st.markdown("##### New Cases")
            plot_metric(
                "Mortality %",
                mortality_percentage,
                prefix="",
                suffix="%",
                show_graph=True,
                color_graph="rgba(255, 43, 43, 0.2)",
            )
        # plot_metric(
        #     "Recovery %",
        #     recovery_percentage,
        #     prefix="",
        #     suffix="%",
        #     show_graph=True,
        #     color_graph="rgba(0, 128, 0, 0.2)",
        # )


with top_right_col1:
    col1, col2 = st.columns((3,1))
    with col2:
        st.write("\n")
        top_n = st.slider('Top countries', min_value=1, max_value=10, value=4, step=1)
    with col1:
        # month_after_map = month_mapping[month]
        # st.markdown(f'#### Top {top_n} Countries by Total {data_type} Cases {month_after_map} {year}')
        st.markdown(f'#### Top {top_n} Countries by Total {data_type} Cases')
        top_countries_df = top_n_countries(covid_df, year, month, continent, column_mapping[data_type], top_n)
        column_name = column_mapping[data_type]
        top_countries_df[column_name] = top_countries_df[column_name].astype(str)
        
        display_top_countries(top_countries_df, column_name, data_type)


with bottom_left_col3:
    st.markdown(f'### COVID-19 Statistics by Continent: {continent}')
    bar_chart = plot_bar(covid_df, year, month, continent)
    st.plotly_chart(bar_chart, use_container_width=True)


with bottom_right_col3:
    # st.markdown(f'#### COVID-19 {data_type} Caases by Days of the Week')
    col1,col2 = st.columns((4,3), gap="medium")
    with col1:
        filtered_jenis_day_data = filter_by_jenis_day(all_covid_df, year, month, continent, column_mapping[data_type])
        donut_chart = plot_donut_chart(filtered_jenis_day_data, column_mapping[data_type])
        st.plotly_chart(donut_chart, use_container_width=True)
    with col2:
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        with st.expander('Info:', expanded=True):
            st.write(f'''
                - Most of Covid-19 :orange[**{data_type} Cases**] are reported on Workdays''')