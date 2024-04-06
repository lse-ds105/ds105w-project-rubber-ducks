import streamlit as st
import json
import datetime
from sqlalchemy import create_engine
import pandas as pd
from plotnine import *

logo_path = "docs/images/RubberDucksLogo.png"

st.set_page_config(
    page_title="Data Analysis",
    page_icon=logo_path,
)

# Create header for the webpage with the name of our project and group logo.
# Use two columns to display the logo next to the text.
col1, col2 = st.columns([1, 4])

with col1:
    st.image(logo_path)
with col2:
    st.markdown("<h1 style='font-size: 80px;'>Data Analysis</h1>", unsafe_allow_html=True)

engine = create_engine('sqlite:///data/rainy.db', echo=False, isolation_level="AUTOCOMMIT")

with engine.connect() as conn:
    pass

"""
# Data Explorer

Select a city, time period and the indicators of your choice:
"""

with open('data/city_coordinates.json', 'r') as f:
    city_dicts = json.load(f)

cities = [city_dict['city'] for city_dict in city_dicts]
variables = pd.read_sql("PRAGMA table_info(weather)", engine)['name'].to_list()
variables = variables[2:]

col1, col2, col3 = st.columns(3)

with col1: 
    city_selection = st.selectbox('City', cities)
    start_date_selection = st.date_input("Start date", value=datetime.date(1940, 1, 1), min_value=datetime.date(1940, 1, 1), max_value=datetime.date(2023, 12, 30))

with col2:
    frequency_selection = st.selectbox("Frequency", ['5 Yearly', 'Yearly', 'Monthly', 'Daily'])
    end_date_selection = st.date_input("End date", value=datetime.date(2023, 12, 31), min_value=datetime.date(1940, 1, 2), max_value=datetime.date(2023, 12, 31))

variables_dict = {
    'temperature_2m_max': 'Max Temperature',
    'temperature_2m_min': 'Min Temperature',
    'temperature_2m_mean': 'Mean Temperature',
    'daylight_duration': 'Daylight Duration (Minutes)',
    'sunshine_duration': 'Daylight Duration (Minutes)',
    'precipitation_sum': 'Total Precipitation (mm)',
    'rain_sum': 'Total Rainfall (mm)',
    'precipitation_hours': 'Precipitation Hours'
}

with col3:
    selected_values = st.multiselect("Indicators", list(variables_dict.values()), default=list(variables_dict.values())[0])

selected_indicators = [
    key for value in selected_values if (key := next((k for k, v in variables_dict.items() if v == value), None))
]


freq_dict = {
    'Monthly': 'M',
    'Yearly': 'Y',
    '5 Yearly': '5Y'
}

if selected_indicators != []:
    query = f"""
        SELECT city, date, {', '.join(selected_indicators)}
        FROM weather
        WHERE city = '{city_selection}'
        AND date BETWEEN '{start_date_selection}' AND '{end_date_selection}';
    """
else:
    query = f"""
        SELECT city, date
        FROM weather
        WHERE city = '{city_selection}'
        AND date BETWEEN '{start_date_selection}' AND '{end_date_selection}';
    """

df = pd.read_sql(query, engine)
df['date'] = pd.to_datetime(df['date'])
df.drop(columns='city', inplace=True)

for column in selected_indicators:
    df[column] = pd.to_numeric(df[column].astype(str).str.replace(',', ''), errors='coerce')

df.set_index('date', inplace=True)

if frequency_selection != 'Daily':
    df = df.resample(freq_dict[frequency_selection]).mean()

df.insert(0, 'city', city_selection)

st.dataframe(df)

if selected_indicators != []:
    g = (
        ggplot(df, aes(x=df.index, y=selected_indicators[0])) +
        geom_point() + 
        labs(x='Date', y=variables_dict[selected_indicators[0]])
    )

    fig = g.draw()

    st.pyplot(fig)