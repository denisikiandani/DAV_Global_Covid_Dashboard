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
# load COVID-19 data
@st.cache_data
def load_covid_data():
    data_path = os.path.join(os.path.dirname(__file__), 'dataset', 'v2_monthly_covid_data.csv')
    df = pd.read_csv(data_path)
    return df

@st.cache_data
def load_all_covid_data():
    data_path = os.path.join(os.path.dirname(__file__), 'dataset', 'v2_all_covid_data.csv')
    df = pd.read_csv(data_path)
    return df

st.set_page_config(
    page_title="Covid-19 Global Statistic Dashboard",
    # page_icon="🏂",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

covid_df = load_covid_data()
all_covid_df = load_all_covid_data()

st.dataframe(all_covid_df)

def pilih_data_type(df, year, month, continent):
    if month == "Entire Year":
        filtered_df = df[df['year'] == year]
        if continent != "All Continent":
            filtered_df = filtered_df[filtered_df['benua'] == continent]
        
        # Sum yearly covid
        filtered_df = filtered_df.groupby('jenis_day', as_index=False).sum()
    else:
        if continent != "All Continent":
            filtered_df = df[(df['year'] == year) & 
                             (df['month'] == month) & 
                             (df['benua'] == continent)]
        else:
            filtered_df = df[(df['year'] == year) & 
                             (df['month'] == month)]
    return filtered_df


def filter_by_jenis_day(df, year, month, continent, data_type):
    filtered_df = pilih_data_type(df, year, month, continent)
    # if month == "Entire Year":
    #     filtered_df = df[df['year'] == year]
    #     if continent != "All Continent":
    #         filtered_df = filtered_df[filtered_df['benua'] == continent]
        
    #     # Sum yearly covid
    #     filtered_df = filtered_df.groupby('jenis_day', as_index=False).sum()
    if data_type == "total_confirmed":
        filtered_df = filtered_df[['jenis_day', 'total_confirmed']]
    elif data_type == "total_recovered":
        filtered_df = filtered_df[['jenis_day', 'total_recovered']]
    elif data_type == "total_deaths":
        filtered_df = filtered_df[['jenis_day', 'total_deaths']]
    else:
        raise ValueError("Invalid data_type. Please choose one of: total_confirmed, total_recovered, total_deaths")
    
    return filtered_df.groupby('jenis_day').sum().reset_index()

lala = filter_by_jenis_day(all_covid_df, 2020, "Entire Year", "Asia", "total_confirmed")
st.dataframe(lala)

pilih_tampil =pilih_data_type(all_covid_df, 2020, "Entire Year", "Asia")
st.dataframe(pilih_tampil)


