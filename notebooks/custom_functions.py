import pandas as pd
import openmeteo_requests
import requests
import urllib

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
    timeseries = df['timeseries'].iloc[0]
    # Creating a DataFrame with year, value, and query
    years = list(range(1940, 2020))
    df_query = pd.DataFrame({'query': query, 'Year': years, 'Appearence %': timeseries})

    # Displaying the final DataFrame
    return df_query