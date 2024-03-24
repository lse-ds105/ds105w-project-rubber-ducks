import pandas as pd
import openmeteo_requests

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