# Rubber Ducks' Project
## Team Members
- Sofia Giorgianni (sogiorgianni) | BSc in Sociology and Statistics
- Oliver Gregory (ollie-gregory) | BSc in Economics
- Noémie Dunand Wisdom (Noemie-DW) | BSc in Economics

## Motivations

- Our motivation for this project is to explore -and potentially _debunk_– the widely held assumption that London is a rainy metropolis. Contrary to popular belief, our experiences living in London suggest maybe it is not as rainy as people believe. By analyzing historical weather data and examining long-term weather trends, we aim to provide a nuanced understanding of London's weather and debunk any misconceptions.
- Ultimately, we hope that this project can promote a more positive narrative surrounding London’s climate.

## How will we get the data?

We plan to use the historical weather API from [open-meteo.com](https://open-meteo.com/en/docs/historical-weather-api#start_date=2024-02-13&end_date=2024-02-24&hourly=rain).

- [open-meteo.com](https://open-meteo.com/en/docs/historical-weather-api#start_date=2024-02-13&end_date=2024-02-24&hourly=rain) is an open source weather API which offers free access for non-commercial users.
- It allows you to request data for different time periods and locations and has a variety of both hourly and daily variables.
- For non-commericial users it has a limit of 10 API calls per day, but we suspect that this shouldn't be a limiting factor for us.
- The website does also supply a code template for accessing the API using python:


## What will we do with the data?

- Firstly, we will focus our analysis on the London scale with bar graphs highlighting the rainiest, sunniest and cloudiest day and month when taking an average year. We will also use a bar graph for every year to see if there is a lot of variance in our results.
- Secundly, to prove the point that London is not the rainiest city, we will extend our analysis to the other 19 most popular cities in the world (using Euromonitor's 2018 ranking). We will compare our measures between all of these cities to come up with rankings. It will also be interesting to show how rankings change over time. This will make sure our hypothesis is consistent and not explained by recent factors such as climate change. 
