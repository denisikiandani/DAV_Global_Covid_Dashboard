import pandas as pd
import streamlit as st

# Read the CSV file
df = pd.read_csv('v2_monthly_covid_data.csv')

# Add a new column for total cases
df['total_cases'] = df['total_confirmed'] + df['total_recovered'] + df['total_deaths']

# Display the first few rows
st.write(df.head())

# Summarize the data
st.write(f"The data covers {df['country/region'].nunique()} countries/regions from {df['year'].min()} to {df['year'].max()}")
st.write(f"The statistics include total confirmed cases, total recovered cases, total deaths, and total cases")

# Group the data by country/region and analyze the trends
for country in df['country/region'].unique():
    country_df = df[df['country/region'] == country]
    
    # Display the country name
    st.write(f"\nAnalysis for {country}:")
    
    # Display the minimum and maximum values for each statistic
    st.write(f"Total confirmed cases: {country_df['total_confirmed'].min()} to {country_df['total_confirmed'].max()}")
    st.write(f"Total recovered cases: {country_df['total_recovered'].min()} to {country_df['total_recovered'].max()}")
    st.write(f"Total deaths: {country_df['total_deaths'].min()} to {country_df['total_deaths'].max()}")
    st.write(f"Total cases: {country_df['total_cases'].min()} to {country_df['total_cases'].max()}")
    
    # Display the entire country DataFrame
    st.write(country_df)
