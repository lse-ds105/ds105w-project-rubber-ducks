import streamlit as st
import pandas as pd

logo_path = "docs/images/RubberDucksLogo.png"

st.set_page_config(
    page_title="Data Collection",
    page_icon=logo_path,
    layout="wide"
)

# Create header for the webpage with the name of our project and group logo.
# Use two columns to display the logo next to the text.
col1, col2 = st.columns([1, 8])

with col1:
    st.image(logo_path)
with col2:
    st.markdown("<h1 style='font-size: 80px;'>Data Collection</h1>", unsafe_allow_html=True)

"""
# Data Pipeline
"""
st.graphviz_chart(
    """
    digraph {
    
    graph [bgcolor=transparent]
    node [shape=box, style="filled,rounded", fillcolor="#333333", fontcolor=white, penwidth="2"]
    edge [color=white, fontcolor=white]

    A [label="open-meteo"]
    L [label="open-meteo API Requests"]
    B [label="London Dataframe"]
    C [label="Bangkok Dataframe"]
    D [label="..."]
    E [label="Hong Kong Dataframe"]
    G [label="Top 20 cities website"]
    H [label="Python list of\n20 cities"]
    I [label="OpenStreetMaps"]
    J [label="OSM API request"]
    K [label="Python list of\ndictionaries for coordinates\nof all cities"]
    X [label="open-meteo API call dictionary"]
    M [label="Weather Dataframe: each row is a time and city"]
    F [label="Save as .csv files"]
    N [label="Google NGRAMS"]
    S [label="JSON format"]
    T [label="Dataframe of appearance % for each NGRAM"]
    U [label="NGRAMS Dataframe"]
    V [label="Final SQL Database"]
    O [label="London Insights: Explore unique visualizations\nfor the vibrant city of London"]
    Q [label="General Trends: Uncover insights and trends\nacross the top 20 most visited cities"]
    W [label="Save as a JSON"]
    
    A -> L
    L -> B
    L -> C
    L -> D
    L -> E
    G -> H [label="scrapy"]
    I -> J
    H -> J
    J -> K
    X -> L
    B -> M
    C -> M
    D -> M
    E -> M
    M -> F [style=dotted]
    N -> S
    S -> T [label="Requests"]
    T -> U [label="Sum each year and divide by a base year"]
    U -> F [style=dotted]
    M -> V
    U -> V
    V -> O
    V -> Q
    K -> W [style=dotted]
    K -> X
}
"""
)

"""
Our final dataset comes from three main sources:
- [OpenMeteo API](https://open-meteo.com/en/docs/historical-weather-api/)
- [Google NGRAMS API](https://books.google.com/ngrams/)
- [Google auto-suggestions API]() ** no link yet
"""

"""
# Data Collection Process
"""

"""
## OpenMeteo API request

### Step 1

Our first task was to scrape the top 20 most vistied cities from [travelness.com](https://travelness.com/most-visited-cities-in-the-world) which we did the old-fashioned way using the ```scrapy``` and ```requests``` libraries in Python.

```python
import requests
from scrapy import Selector

cities_url = "https://travelness.com/most-visited-cities-in-the-world" # URL of the page with the list of cities

response = requests.get(cities_url)
sel = Selector(response)

cities = sel.xpath("//table//tr/td[2]/text()").getall()
```

This simply returns a list of the top 20 most visited cities:
```python
['Bangkok', 'Paris', 'London', 'Dubai', 'Singapore', 'Kuala Lumpur', 'New York', 'Istanbul', 'Tokyo', 'Antalya', 'Seoul', 'Osaka', 'Makkah', 'Phuket', 'Pattaya', 'Milan', 'Barcelona', 'Palma de Mallorca', 'Bali', 'Hong Kong SAR']
```

### Step 2

The next stage along in our journey was to geocode the cities so that we were able to input the coordinates into the [OpenMeteo API](https://open-meteo.com/en/docs/historical-weather-api/) as that is what it requires. We accomplished this through the use of the [OpenStreetMaps API](https://wiki.openstreetmap.org/wiki/API) which, while effective, was not the most efficient and took roughly 40s to complete.

```python
from geopy.geocoders import Nominatim

def geocode_city(city):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(city)
    return {"city": city, "latitude": location.latitude, "longitude": location.longitude}

def geocode_cities(city_list):
    geocoded_cities = [geocode_city(city) for city in city_list if geocode_city(city)]
    return geocoded_cities

# Geocode the list of cities
geocoded_cities = geocode_cities(cities)
```

This returned a list of dictionaries that we then exported as a JSON file - here is a clipping of the first three cities:
"""

st.json([{"city": "Bangkok", "latitude": -7.33495, "longitude": 110.6589317}, {"city": "Paris", "latitude": 48.8534951, "longitude": 2.3483915}, {"city": "London", "latitude": 51.4893335, "longitude": -0.14405508452768728}])

"""
We then used this data to prepare the ```params``` argument in the OpenMeteo API request along with a list of our desired variables.

```python
params = {
    "latitude": [city["latitude"] for city in geocoded_cities],
    "longitude": [city["longitude"] for city in geocoded_cities],
    "start_date": "1940-01-01",
    "end_date": "2023-12-31",
    "daily": daily_variables_of_interest,
}
```

### Step 3

Only now were we finally ready for the actual API call where we created a custom function ```process_response()``` using the API documentation that processed each response into a pandas dataframe before we merged them and exported it as a CSV.

```python
# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"
responses = openmeteo.weather_api(url, params=params)

dataframes_list = [cf.process_response(response, geocoded_cities, i) for i, response in enumerate(responses)]
merged_df = pd.concat(dataframes_list, ignore_index=True)
merged_df.to_csv("../data/weather_data.csv", index=False)
```
Here are the first 20 rows for your enjoyment (there are 600,000 total):
"""
df = pd.read_csv('data/weather_data.csv').head(20) # update file path when in the github repository.

st.dataframe(df)

"""

## Google NGRAMS API request
"""

"""
## Google auto-suggestions API request
"""