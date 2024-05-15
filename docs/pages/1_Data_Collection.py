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

    P [label="Google autosuggestions API"]
    R [label="Perception Wordclouds"]
    Y [label="Save as a JSON"]

    
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
    K -> P
    P -> Y
    Y -> R
}
"""
)

"""
Our final dataset comes from three main sources:
- [OpenMeteo API](https://open-meteo.com/en/docs/historical-weather-api/)
- [Google NGRAMS API](https://books.google.com/ngrams/)
- Google auto-suggestions API
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

NGRAM queries on Google NGRAMS allow the user to see the percentage of times a query appears amongts all the words and phrases accounted for in the books available on Google Books. In our case, we want to retrieve data on the perceptions of rain, sun and wind in London.

### Step 1

We started off by making a list of the queries we wanted to run for each weather variable: rain, sun and wind. We alternated between capitalised and uncapitalised letters where it was reasonable to do so, in order to collect as much relevant data as possible.

```python
queries_rain = ["London rain", "London Rain", "rainy London", "rain in London", "Rain in London", "raining in London", "Raining in London"]
queries_sun = ["London sun", "London Sun", "sunny London", "sun in London", "Sun in London"]
queries_wind = ["London wind", "London Wind", "windy London", "wind in London", "Wind in London"]
```

### Step 2

We created the custom ```get_NGRAMS``` function, which extracts the appearance percentages from 1940 to 2019 for a single query and converts the response into a pandas dataframe as it initally comes in JSON format.

```python
def get_NGRAMS(query):
    # converting a regular string to  the standard URL format  
    query_url = urllib.parse.quote(query) 

    # creating the URL 
    url = 'https://books.google.com/ngrams/json?content=' + query_url +'&year_start=1940&corpus=en-2019&smoothing=3' 
    response = requests.get(url) 

    # extracting the json data from the response we got 
    output = response.json()

    # Extracting the timeseries
    timeseries = output[0]['timeseries']

    # Creating a DataFrame with year, value, and query
    years = list(range(1940, 2020))
    df_query = pd.DataFrame({'query': query, 'year': years, 'appearances': timeseries})

    return df_query
```

We then used a ```for``` loop to iterate through each query before merging each query dataframe into one.

```python
NGRAMSrain_df = pd.DataFrame()
queries_rain = ["London rain", "London Rain", "rainy London", "rain in London", "Rain in London", "raining in London", "Raining in London"]

for query in queries_rain:
    df_queries_rain = cf.get_NGRAMS(query)
    NGRAMSrain_df = pd.concat([NGRAMSrain_df, df_queries_rain])
```

We end up with 3 dataframes: NGRAMSrain_df, NGRAMSsun_df and NGRAMSwind_df.

### Step 3
In each dataframe, we summed up all different queries' appearances for each year. This enabled us to have a general perception for a given year. The associated new dataframes were named NGRAMSrain_df_grouped, NGRAMSsun_df_grouped and NGRAMSwind_df_grouped.

### Step 4
We then created a new column which represents the relative appearance percentages. This was done by dividing percentages in each row by the first row. The column brings a clearer image of the change in these perceptions.

### Step 5
We merged the 3 dataframes into one general perception dataframe NGRAMS_df_grouped. It organises data on absolute and relative appearance percentages for rain, wind, and sun queries from 1940 to 2019.

"""

df = pd.read_csv('data/perception_data.csv')

st.dataframe(df)

"""
Absolute percentages are so low that they are ≈ 0.
"""

"""
## Google auto-suggestions API request

After getting the top 20 most vistied cities, we can get the auto suggestions for each city from google to see what stereotypes people have about that city using the requests library.

### Step 1

We use two queries in this function to make the result richer.

**TIP:**
 'Hong Kong SAR' is a term that emphasizes the administrative characteristic of the city, and it is rarely used in everyday life. Therefore, it is changed into 'Hong Kong' in this function to suit the spoken language.

```python
import requests

def get_auto_suggestions(city):
    adjusted_city = 'Hong Kong' if city == 'Hong Kong SAR' else city
    queries = [f"why is {adjusted_city} so", f"why is {adjusted_city} always"]
    
    all_suggestions = []
    for query in queries:
        url = f"https://www.google.com/complete/search?q={query}&client=firefox"
        response = requests.get(url)
        if response.status_code == 200:
            suggestions = response.json()[1]
            all_suggestions.extend(suggestions)
        else:
            print(f"Fail: {query}")
    return all_suggestions
```

This returns a list of simple sentences that needs to be processed. Here is the example of London:

```python
['why is london so expensive', 'why is london so dangerous', 'why is london so popular', 'why is london so big', 'why is london so foggy', 'why is london so busy today', 'why is london so dirty', 'why is london so cold', 'why is london so cloudy', 'why is london so rainy', 'why is london always cloudy', 'why is london always rainy', 'why is london always cold', 'why is london always foggy', 'why is london always grey', 'why is london always raining', 'why is london always so cloudy', 'why is london always windy', 'why is london always gray', 'why is london always hotter']
```

### Step 2

We then need to scrape all the 20 cities and extract the discriptive words in such lists which makes the output neat and clean. In this function, the ```re``` library is used to locate the position of those discriptive words.

```python
import re

def extract_words(cities):
    city_stereotype = {}
    for city in cities:
        suggestions = get_auto_suggestions(city)
        stereotype_list = [] 
        for suggestion in suggestions:
            if 'why' in suggestion.lower() and ('so' in suggestion.lower() or 'always' in suggestion.lower()):
                suggestion_parts = {}
                for delimiter in ['so', 'always']:
                    suggestion_parts[delimiter] = re.split(fr'\b{delimiter}\b', suggestion)
                    if len(suggestion_parts[delimiter]) > 1:
                        stereotype = suggestion_parts[delimiter][1].strip()
                        stereotype_list.append(stereotype)
        full_stereotype_str = ', '.join(stereotype_list)
        city_stereotype[city] = full_stereotype_str
    return city_stereotype
```

### Step 3

Finally, we use this function to filter the words that are about weather before returning a dictionary that only contains the words we are interested in.

```python
def filter_weather_words(suggestion_dict):
    weather_words = ["sunny", "rainy", "windy", "cloudy", "foggy", "hot", "cold", "stormy", "humid", "dry", "wet"]
    new_dict = {}
    for key, words_str in suggestion_dict.items():
        words_list = words_str.split(', ')
        filtered_word_list = [word for word in words_list if word in weather_words]
        new_dict[key] = filtered_word_list
    return new_dict
```

"""