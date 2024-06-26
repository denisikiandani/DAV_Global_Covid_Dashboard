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

# load COVID-19 data
@st.cache_data
def load_covid_data():
    data_path = os.path.join(os.path.dirname(__file__), 'dataset', 'v2_monthly_covid_data.csv')
    df = pd.read_csv(data_path)
    return df

# load GeoJSON data
@st.cache_data
def load_geojson_data():
    geojson_path = os.path.join(os.path.dirname(__file__), 'geo_dataset', 'countries.geo.json')
    with open(geojson_path) as f:
        geojson_data = json.load(f)
    gdf = gpd.GeoDataFrame.from_features(geojson_data)
    return gdf, geojson_data


def pilih_data_type(df, year, month, continent):
    if month == "Entire Year":
        filtered_df = df[df['year'] == year]
        if continent != "All Continent":
            filtered_df = filtered_df[filtered_df['benua'] == continent]
        
        # Sum yearly covid
        filtered_df = filtered_df.groupby('country/region', as_index=False).sum()
    else:
        if continent != "All Continent":
            filtered_df = df[(df['year'] == year) & 
                             (df['month'] == month) & 
                             (df['benua'] == continent)]
        else:
            filtered_df = df[(df['year'] == year) & 
                             (df['month'] == month)]
    return filtered_df
    
def filter_data(df, year, month, continent, data_type):
    filtered_df = pilih_data_type(df, year, month, continent)
        
    if data_type == "total_confirmed":
        filtered_df = filtered_df[['country/region', 'total_confirmed']]
    elif data_type == "total_recovered":
        filtered_df = filtered_df[['country/region', 'total_recovered']]
    elif data_type == "total_deaths":
        filtered_df = filtered_df[['country/region', 'total_deaths']]
    else:
        raise ValueError("Invalid data_type. Please choose one of: total_confirmed, total_recovered, total_deaths")
    
    return filtered_df

def filter_cases(df, year, month, continent):
    filtered_df = pilih_data_type(df, year, month, continent)
    
    # Ensure necessary columns exist
    if 'total_confirmed' not in filtered_df.columns:
        filtered_df['total_confirmed'] = 0
    if 'total_recovered' not in filtered_df.columns:
        filtered_df['total_recovered'] = 0
    if 'total_deaths' not in filtered_df.columns:
        filtered_df['total_deaths'] = 0
        
    all_total_confirmed = filtered_df['total_confirmed'].sum()
    all_total_recovered = filtered_df['total_recovered'].sum()
    all_total_deaths = filtered_df['total_deaths'].sum()
    total_cases = all_total_confirmed + all_total_recovered + all_total_deaths
    return all_total_confirmed, all_total_recovered, all_total_deaths, total_cases

def plot_gauge(indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 20,
            },
            gauge={
                "axis": {
                    "range": [0, max_bound], 
                    "showticklabels": False,
                    # "tickwidth": 0,  # Set tick width to 0 to hide ticks
                    # "tickcolor": "rgba(0,0,0,0)",  # Set tick color to transparent
                },
                "bar": {
                    "color": indicator_color,
                    "thickness": 1, 
                },
            },
            title={
                "text": indicator_title,
                "font": {"size": 15},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=125,
        margin=dict(l=10, r=25, t=0, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)
    