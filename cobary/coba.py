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




# Load the data
df = pd.read_csv('v2_monthly_covid_data.csv')

# Prepare the data for the seasonal distribution plot
df['Date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str), format='%Y-%m')
df['Season'] = pd.cut(df['month'], bins=[-1, 2, 5, 8, 11, 14], labels=['Winter', 'Spring', 'Summer', 'Autumn', 'Dry Season'])

# Create the seasonal distribution plot
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='Date', y='total_confirmed', hue='Season', data=df)
plt.xlabel('Date')
plt.ylabel('Total Confirmed Cases')
plt.title('Distribution of Covid 19 per Season')
plt.legend()

# Display the plot in Streamlit
st.pyplot(fig)





# Load the data from the CSV file
df = pd.read_csv('v2_monthly_covid_data.csv')

# Sort the data by the 'total_confirmed' column in descending order
top_5_confirmed = df.sort_values(by='total_confirmed', ascending=False).head(5)

# Display the top 5 confirmed cases
st.write("Top 5 Confirmed Cases:")
st.write(top_5_confirmed)