import pandas as pd
import streamlit as st

# Load the CSV file
file_path = r'C:\Users\Shandra Manuaba\Documents\SEMESTER 6\Data Analytics & Visualization\New folder\DAV_Global_Covid_Dashboard\streamlit\dataset\v2_monthly_covid_data.csv'
data = pd.read_csv(file_path)

# Ensure the necessary columns exist
required_columns = ['country/region', 'total_confirmed', 'total_recovered']
if all(column in data.columns for column in required_columns):
    # Calculate recovery rate
    data['recovery_rate'] = data['total_recovered'] / data['total_confirmed'] * 100

    # Get top 5 countries with highest recovery rates
    top_5_countries = data.nlargest(5, 'recovery_rate')

    # Streamlit app
    st.title("Top 5 Countries with Highest COVID-19 Recovery Rates")

    st.write("This app displays the top 5 countries with the highest COVID-19 recovery rates.")

    st.write("### Top 5 Countries")
    st.dataframe(top_5_countries[['country/region', 'recovery_rate']])

    # Display additional details if required
    st.write("### Detailed Information")
    st.dataframe(top_5_countries)
else:
    st.write("The required columns are not present in the dataset.")
