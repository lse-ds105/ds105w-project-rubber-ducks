import streamlit as st
import json
import datetime
from sqlalchemy import create_engine
import pandas as pd

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

col1, col2, col3 = st.columns(3)

with col1: 
    start_date_selection = st.date_input("Start date", value=datetime.date(1940, 1, 1), min_value=datetime.date(1940, 1, 1), max_value=datetime.date(2023, 12, 30))
    end_date_selection = st.date_input("End date", value=datetime.date(2023, 12, 31), min_value=datetime.date(1940, 1, 2), max_value=datetime.date(2023, 12, 31))

with col2:
    city_selection = st.selectbox('City', cities)

with col3:
    indicators = st.multiselect("Indicators", variables)