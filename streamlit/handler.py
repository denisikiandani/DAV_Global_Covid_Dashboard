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

@st.cache_data
def load_all_covid_data():
    data_path = os.path.join(os.path.dirname(__file__), 'dataset', 'v2_all_covid_data.csv')
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


def top_n_countries(df, year, month, continent, data_type, n):
    filtered_df = pilih_data_type(df, year, month, continent)
    
    if data_type == "total_confirmed":
        filtered_df = filtered_df[['country/region', 'total_confirmed']]
    elif data_type == "total_recovered":
        filtered_df = filtered_df[['country/region', 'total_recovered']]
    elif data_type == "total_deaths":
        filtered_df = filtered_df[['country/region', 'total_deaths']]
    else:
        raise ValueError("Invalid data_type. Please choose one of: total_confirmed, total_recovered, total_deaths")
    
    filtered_df = filtered_df.sort_values(by=data_type, ascending=False)
    
    top_countries = filtered_df.head(n)
    return top_countries

def new_prev_year(df, year, month, continent):
    if month == "Entire Year":
        current_year_data = df[df['year'] == year]
        previous_year_data = df[df['year'] == (year - 1)]
    else:
        current_year_data = df[(df['year'] == year) & (df['month'] == month)]
        previous_month = month - 1 if month > 1 else 12
        previous_year = year if month > 1 else year - 1
        previous_year_data = df[(df['year'] == previous_year) & (df['month'] == previous_month)]

    if continent != "All Continent":
        current_year_data = current_year_data[current_year_data['benua'] == continent]
        previous_year_data = previous_year_data[previous_year_data['benua'] == continent]
    
    return current_year_data, previous_year_data

def calculate_new(df, year, month, continent):
    current_year_data, previous_year_data = new_prev_year(df, year, month, continent)
        
    current_totals = current_year_data.groupby('country/region').sum().sum()
    previous_totals = previous_year_data.groupby('country/region').sum().sum()
    
    new_confirmed = current_totals['total_confirmed'] - previous_totals['total_confirmed']
    new_deaths = current_totals['total_deaths'] - previous_totals['total_deaths']
    new_cases = new_confirmed + (current_totals['total_recovered'] - previous_totals['total_recovered']) + new_deaths
    recovery_percentage = (current_totals['total_recovered'] / current_totals['total_confirmed']) * 100 if current_totals['total_confirmed'] != 0 else 0
    mortality_percentage = (current_totals['total_deaths'] / current_totals['total_confirmed']) * 100 if current_totals['total_confirmed'] != 0 else 0
    
    return new_cases, new_confirmed, new_deaths, recovery_percentage, mortality_percentage

def display_covid_dataframe(df, year, month, continent):
    current_year_data, previous_year_data = new_prev_year(df, year, month, continent)
    if month == "Entire Year":
        current_totals = current_year_data.groupby(['country/region']).agg({
            'total_confirmed': 'sum',
            'total_recovered': 'sum',
            'total_deaths': 'sum',
            'benua': 'first',
        }).reset_index()

        previous_totals = previous_year_data.groupby(['country/region']).agg({
            'total_confirmed': 'sum',
            'total_recovered': 'sum',
            'total_deaths': 'sum',
            'benua': 'first',
        }).reset_index()
    else:
        current_totals = current_year_data.groupby(['country/region']).agg({
            'total_confirmed': 'sum',
            'total_recovered': 'sum',
            'total_deaths': 'sum',
            'benua': 'first',
        }).reset_index()

        previous_totals = previous_year_data.groupby(['country/region']).agg({
            'total_confirmed': 'sum',
            'total_recovered': 'sum',
            'total_deaths': 'sum',
            'benua': 'first',
        }).reset_index()

    # Ensure previous_totals has the same structure even if empty
    if previous_totals.empty:
        previous_totals = current_totals.copy()
        previous_totals[['total_confirmed', 'total_recovered', 'total_deaths']] = 0

    merged_totals = current_totals.merge(previous_totals, on='country/region', suffixes=('_current', '_previous'), how='left')

    # Fill NaN values with 0 to avoid calculation errors
    merged_totals = merged_totals.fillna(0)

    new_confirmed = merged_totals['total_confirmed_current'] - merged_totals['total_confirmed_previous']
    new_deaths = merged_totals['total_deaths_current'] - merged_totals['total_deaths_previous']
    new_recovered = merged_totals['total_recovered_current'] - merged_totals['total_recovered_previous']
    new_cases = new_confirmed + new_recovered + new_deaths
    recovery_percentage = (merged_totals['total_recovered_current'] / merged_totals['total_confirmed_current']) * 100
    mortality_percentage = (merged_totals['total_deaths_current'] / merged_totals['total_confirmed_current']) * 100
    
    recovery_percentage = recovery_percentage.fillna(0).round(2)
    mortality_percentage = mortality_percentage.fillna(0).round(2)
    result_df = pd.DataFrame({
        'Country or Region': merged_totals['country/region'],
        'New Cases': new_cases.values,
        'New Confirmed': new_confirmed.values,
        'New Deaths': new_deaths.values,
        'Recovery %': recovery_percentage.values,
        'Mortality %': mortality_percentage.values
    })
    
    result_df = result_df.sort_values(by='New Cases', ascending=False).reset_index(drop=True)
    result_df.index += 1
    st.dataframe(result_df,
            column_order=("Country or Region", 'New Cases', 'New Confirmed', 'New Deaths', 'Recovery %', 'Mortality %'),
            hide_index=True,
            # width=None,
            column_config={
                "country/region": st.column_config.TextColumn("Country"),
                # "New Cases": st.column_config.ProgressColumn(
                #     "New Cases",
                #     format="%d",
                #     min_value=0,
                #     max_value=df["New Cases"].max(),
                # )
            })
    
    # result_df = result_df.sort_values(by='New Cases', ascending=False).reset_index(drop=True)
    # result_df.index += 1
    # return result_df

def filter_by_jenis_day(df, year, month, continent, data_type):
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
            
    if data_type == "total_confirmed":
        filtered_df = filtered_df[['jenis_day', 'total_confirmed']]
    elif data_type == "total_recovered":
        filtered_df = filtered_df[['jenis_day', 'total_recovered']]
    elif data_type == "total_deaths":
        filtered_df = filtered_df[['jenis_day', 'total_deaths']]
    else:
        raise ValueError("Invalid data_type. Please choose one of: total_confirmed, total_recovered, total_deaths")
    
    return filtered_df.groupby('jenis_day').sum().reset_index()

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


def display_top_countries(df, column_name, data_type):
    st.dataframe(df,
            column_order=("country/region", column_name),
            hide_index=True,
            # width=None,
            column_config={
                "country/region": st.column_config.TextColumn("Country"),
                column_name: st.column_config.ProgressColumn(
                    f"Total {data_type}",
                    format="%d",
                    min_value=0,
                    max_value=df[column_name].max(),
                )
            })

def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 20,
            },
            title={
                "text": label,
                "font": {"size": 10},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=10, b=0),
        showlegend=False,
        # plot_bgcolor="black",
        height=50,
        # width=150,
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_bar(df, year, month, continent):
    if month == "Entire Year":
        filtered_df = df[df['year'] == year]
        if continent != "All Continent":
            filtered_df = filtered_df[filtered_df['benua'] == continent]
        
        # Sum yearly covid
        filtered_df = filtered_df.groupby('benua', as_index=False).sum()
    else:
        if continent != "All Continent":
            filtered_df = df[(df['year'] == year) & 
                             (df['month'] == month) & 
                             (df['benua'] == continent)]
        else:
            filtered_df = df[(df['year'] == year) & 
                             (df['month'] == month)]
    
    fig = px.bar(
        filtered_df,
        x="benua",  # Assuming "benua" is your column for continents
        y=["total_confirmed", "total_recovered", "total_deaths"],
        barmode="group",
        labels={"benua": "Continent", "value": "Count", "variable": "Category"},
    )
    
    fig.update_layout(
        xaxis_title="Continent",
        yaxis_title="Count",
        legend_title="Category",
        height=400,  # Set height of the plot
        width=500,   # Set width of the plot
    )
    
    return fig

def plot_donut_chart(df, data_type):
    custom_colors = ['#7BCCC4', '#08589E']

    fig = px.pie(
        df, 
        names='jenis_day', 
        values=data_type, 
        hole=0.3,
        title="LALLAL HTIKU KACU"
    )

    # Update warna dan hilangkan legend
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(colors=custom_colors)  # Menggunakan daftar warna custom
    )
    fig.update_layout(
        showlegend=False,  # Menghilangkan legend
        margin=dict(t=0, b=0, l=0, r=0)  # Mengatur margin, top (t), bottom (b), left (l), right (r)
    )

    return fig