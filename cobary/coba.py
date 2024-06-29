import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('v2_monthly_covid_data.csv')

# Add a new column for total cases
df['total_cases'] = df['total_confirmed'] + df['total_deaths'] + df['total_recovered']

# Set up the dashboard
st.set_page_config(layout="wide")
st.title("COVID-19 Global Statistics")

# Display the country distribution
st.subheader("Distribution of Covid 19 per Country")
st.dataframe(df)