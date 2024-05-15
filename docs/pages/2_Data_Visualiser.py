import streamlit as st
import json
import datetime
from sqlalchemy import create_engine
import pandas as pd
from plotnine import *

logo_path = "docs/images/RubberDucksLogo.png"

st.set_page_config(
    page_title="Data Visualiser",
    page_icon=logo_path,
    layout="wide"
)

# Create header for the webpage with the name of our project and group logo.
# Use two columns to display the logo next to the text.
col1, col2 = st.columns([1, 8])

with col1:
    st.image(logo_path)
with col2:
    st.markdown("<h1 style='font-size: 80px;'>Data Visualiser</h1>", unsafe_allow_html=True)

# Create a database engine
engine = create_engine('sqlite:///data/rainy.db', echo=False, isolation_level="AUTOCOMMIT")

with engine.connect() as conn:
    pass

## Define variables and dictionaries for the data explorer and visualiser.
# Read the city coordinates json to get the list of cities we have data on.
with open('data/city_coordinates.json', 'r') as f:
    city_dicts = json.load(f)

cities = [city_dict['city'] for city_dict in city_dicts]

# Create a dictionary of variables available for analysis so variable names are less confusing to the user.
variables_dict = {
    'Max Temperature': 'temperature_2m_max',
    'Min Temperature': 'temperature_2m_min',
    'Mean Temperature': 'temperature_2m_mean',
    'Daylight Duration (Minutes)': 'daylight_duration',
    'Sunshine Duration (Minutes)': 'sunshine_duration',
    'Total Precipitation (mm)': 'precipitation_sum',
    'Total Rainfall (mm)': 'rain_sum',
    'Precipitation Hours': 'precipitation_hours'
}

# Create a dictionary of frequencies available for analysis.
freq_dict = {
    'Monthly': 'M',
    'Yearly': 'Y',
    '5 Yearly': '5Y'
}

explorerTab, visualiserTab, wordcloudTab = st.tabs(["Explorer", "Visualiser", "Wordcloud"])

with explorerTab:
    """
    # Weather Data Explorer

    Select a city, time period and the indicators of your choice:
    """

# Create the data explorer options selector.
    col1, col2, col3 = st.columns(3)

    with col1: 
        city_selection_de = st.selectbox('City', cities)
        start_date_selection_de = st.date_input("Start date", value=datetime.datetime(1940, 1, 1), min_value=datetime.datetime(1940, 1, 1), max_value=datetime.datetime(2023, 12, 30))

    end_date_selection_de_min = start_date_selection_de + datetime.timedelta(days=1)

    with col2:
        frequency_selection_de = st.selectbox("Frequency", ['5 Yearly', 'Yearly', 'Monthly', 'Daily'])
        end_date_selection_de = st.date_input("End date", value=datetime.date(2023, 12, 31), min_value=end_date_selection_de_min, max_value=datetime.date(2023, 12, 31))

    with col3:
        selected_keys_de = st.multiselect("Indicators", list(variables_dict.keys()), default=list(variables_dict.keys())[0])

# Convert the list of selected indicators into their variable names.
    selected_indicators_de = [variables_dict[key] for key in selected_keys_de]

## Create the custom dataframe.
# Generate the query for the database:
    if selected_indicators_de != []:
        query = f"""
            SELECT city, date, {', '.join(selected_indicators_de)}
            FROM weather
            WHERE city = '{city_selection_de}'
            AND date BETWEEN '{start_date_selection_de}' AND '{end_date_selection_de}';
        """
    else:
        query = f"""
            SELECT city, date
            FROM weather
            WHERE city = '{city_selection_de}'
            AND date BETWEEN '{start_date_selection_de}' AND '{end_date_selection_de}';
        """

# Read in the database to a dataframe
    df = pd.read_sql(query, engine)

# Set the date column to datetime format
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

# Drop the city column so when resampling, each column is numeric (except for the date).
    df.drop(columns='city', inplace=True)

# Convert columns to numeric format.
    for column in selected_indicators_de:
        df[column] = pd.to_numeric(df[column].astype(str).str.replace(',', ''), errors='coerce')

# Resample the data if needed.
    if frequency_selection_de != 'Daily':
        df = df.resample(freq_dict[frequency_selection_de]).mean()

# Add the city back to the dataframe
    df.insert(0, 'city', city_selection_de)

# Display the custom dataframe
    st.dataframe(df)

with visualiserTab:

    """
    # Weather Data Visualiser

    Select a city, time period and the indicator of your choice:
    """

# Create a dictionary of the plotting options available.
    plot_dict = {
        'Scatter': geom_point(size=5),
        'Line': geom_line(size=3),
        'Bar': geom_col(),
    }

# Create the data visualiser options selector.
    col1, col2, col3 = st.columns(3)

    with col1: 
        city_selection_dv = st.selectbox('City', cities, key='dv_city')
        start_date_selection_dv = st.date_input("Start date", value=datetime.datetime(1940, 1, 1), min_value=datetime.datetime(1940, 1, 1), max_value=datetime.datetime(2023, 12, 30), key='dv_start')

    end_date_selection_dv_min = start_date_selection_dv + datetime.timedelta(days=1)

    with col2:
        frequency_selection_dv = st.selectbox("Frequency", ['5 Yearly', 'Yearly', 'Monthly', 'Daily'], key='dv_freq')
        end_date_selection_dv = st.date_input("End date", value=datetime.date(2023, 12, 31), min_value=end_date_selection_dv_min, max_value=datetime.date(2023, 12, 31), key='dv_end')

    with col3:
        selected_key_dv = st.selectbox("Indicators", list(variables_dict.keys()), key='dv_indicator')
        plot_option = st.selectbox("Plot type", ['Scatter', 'Line', 'Bar'])
        plot_type = plot_dict[plot_option]

    selected_indicator_dv = variables_dict[selected_key_dv]
## Create the custom dataframe.
# Generate the query for the database:
    query = f"""
            SELECT city, date, {selected_indicator_dv}
            FROM weather
            WHERE city = '{city_selection_dv}'
            AND date BETWEEN '{start_date_selection_dv}' AND '{end_date_selection_dv}';
        """

# Read in the database to a dataframe
    df = pd.read_sql(query, engine)

# Set the date column to datetime format
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

# Drop the city column so when resampling, each column is numeric (except for the date).
    df.drop(columns='city', inplace=True)

# Convert columns to numeric format.
    df[selected_indicator_dv] = pd.to_numeric(df[selected_indicator_dv].astype(str).str.replace(',', ''), errors='coerce')

# Resample the data if needed.
    if frequency_selection_dv != 'Daily':
        df = df.resample(freq_dict[frequency_selection_dv]).mean()

# Add the city back to the dataframe
    df.insert(0, 'city', city_selection_dv)

# Create the plot
    g = (
        ggplot(df, aes(x=df.index, y=selected_indicator_dv, color=selected_indicator_dv, fill=selected_indicator_dv)) +
        plot_type +
        labs(x='Date', y=selected_key_dv) +
        theme_minimal() +
        theme(text=element_text(color="white"),line=element_line(color="white"), figure_size=(10,6))
    )

# Draw the plot for use with the streamlit.pyplot() function.
    fig = g.draw()

    col1, col2, col3 = st.columns([1,6,1]) # Use columns to adjust size of plot on website.
    with col2:
        st.pyplot(fig)

with wordcloudTab:
    city_wc = st.selectbox("Select a city to view its perception word cloud from Google Autosuggestions", (cities), key='wc_city')

    st.write(f"# Wordcloud for {city_wc}")

    image_path = f"./docs/images/wordclouds/{city_wc}.png"

    st.image(image_path, use_column_width=True)