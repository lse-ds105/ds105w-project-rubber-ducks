import pandas as pd
import openmeteo_requests
import requests
import urllib
import re

def process_response(response, geocoded_cities, i):
    daily = response.Daily()
    temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    temperature_2m_mean = daily.Variables(2).ValuesAsNumpy()
    daylight_duration = daily.Variables(3).ValuesAsNumpy()
    sunshine_duration = daily.Variables(4).ValuesAsNumpy()
    precipitation_sum = daily.Variables(5).ValuesAsNumpy()
    rain_sum = daily.Variables(6).ValuesAsNumpy()
    precipitation_hours = daily.Variables(7).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ).date
    }

    daily_data["city"] = geocoded_cities[i]['city']
    daily_data["temperature_2m_max"] = temperature_2m_max
    daily_data["temperature_2m_min"] = temperature_2m_min
    daily_data["temperature_2m_mean"] = temperature_2m_mean
    daily_data["daylight_duration"] = daylight_duration
    daily_data["sunshine_duration"] = sunshine_duration
    daily_data["precipitation_sum"] = precipitation_sum
    daily_data["rain_sum"] = rain_sum
    daily_data["precipitation_hours"] = precipitation_hours

    return pd.DataFrame(data=daily_data)

def runQuery(query):
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
    df_query = pd.DataFrame({'query': query, 'Year': years, 'Absolute Appearance %': timeseries})

    # Displaying the final DataFrame
    return df_query

# Create a list of stereotypes given by google auto suggestions
def get_auto_suggestions(city):
    # 'Hong Kong SAR' is a term that emphasizes the administrative characteristic of the city
    # And it is rarely used in everyday life, so in order to suit the Google Auto Suggestions
    # it is changed into 'Hong Kong' in this function
    adjusted_city = 'Hong Kong' if city == 'Hong Kong SAR' else city
    
    #There are more suggestions about weather in the second query, but some cities have no result in the second one
    #So we use two queries to make the function better
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
    
# Extract the discriptive words of the suggestions and create a dictionary
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

def filter_weather_words(suggestion_dict):
    weather_words = ["sunny", "rainy", "windy", "cloudy", "foggy", "hot", "cold", "stormy", "humid", "dry", "wet"]
    new_dict = {}
    for key, words_str in suggestion_dict.items():
        words_list = words_str.split(', ')
        filtered_word_list = [word for word in words_list if word in weather_words]
        new_dict[key] = filtered_word_list
    return new_dict