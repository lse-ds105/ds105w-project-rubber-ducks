import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

logo_path = "docs/images/RubberDucksLogo.png"

engine = create_engine('sqlite:///data/rainy.db', echo=False, isolation_level="AUTOCOMMIT")

with engine.connect() as conn:
    pass

st.set_page_config(
    page_title="Key Insights",
    page_icon=logo_path,
    layout="wide"
)

# Create header for the webpage with the name of our project and group logo.
# Use two columns to display the logo next to the text.
col1, col2 = st.columns([1, 8])

with col1:
    st.image(logo_path)
with col2:
    st.markdown("<h1 style='font-size: 80px;'>Key Insights</h1>", unsafe_allow_html=True)

'''
# _Is London a rainy city?_

This was the central question our group set out to answer, so what have we found?

'''

st.divider()

'''
### How has the perception of London changed since 1940?
'''

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.image('docs/images/london_rain_perception.svg')

with col2:
    st.markdown(
        '''
        This graph shows that in the 1940s, the rainy London stereotype had a relatively low prevalence. It then experienced some fluctuation, with a peak around 1965; however, starting from around the year 2000, there was a significant rise in the prevalence of this stereotype, reaching its highest point in recent times around 2010. The overall shape of the graph suggests that while the stereotype has existed for a long time, it has become much more prominent and widespread in recent decades, particularly from the turn of the 21st century onwards. This could potentially be a result of various factors, such as media representation, cultural perceptions, or even actual weather patterns in London during this period.
        '''
    )

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        '''
        In the early years post 1940, average precipitation hours were higher than in the post 2000s, yet the perception of London as a rainy city in literature was lowest around 1940 and highest around 2019. This shows how perception of London as a rainy city and the actual weather facts are negatively correlated, and that this stereotype is not justified by precipitation hours.
        '''
    )

with col2:
    st.image('docs/images/london_precipitation_vs_perception.svg')

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.image('docs/images/london_sun_vs_perception.svg')

with col2:
    st.markdown(
        '''
        When comparing how sunny London is relative to its perception in literature as a sunny place, we see that since 1940, the perception of London as a sunny city has steadily increased but by nowhere near as much as the perception of it as a rainy city. When looking at how sunny London actually is though, we see that it has been fairly consitent with only a noticeable dip between the late 60s and early 90s.
        '''
    )

st.divider()

'''
### How does the weather in London compare to the rest of the world?
'''

st.divider()

col1, col2 = st.columns(2)

with col1:
    '''
    When comparing the average amount of rain that falls in London to the rest of the twenty most visited cities, we see that London is only fourth from the bottom with a pitiful average of less than 2mm of rain a day. In contrast, Bali, the rainiest, gets over four times as much rain as London. Perhaps then, the stereotype comes not from how much rain falls in London but for how long it rains instead?
    '''

with col2:
    st.image('docs/images/precipitation_sum_bar.svg')

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.image('docs/images/precipitation_hours_bar.svg')

with col2:
    '''
    Here we can see that the average daily hours of rainfall in London since 1940 is just under 4 hours, which pales in comparison to cities such as Singapore and Phuket which are much closer to an average of 10 hours a day. This implies that justifying the perception of London as a rainy city by suggesting that it doesn't rain heavily but just drizzles all the time is also an invalid argument given it is not even in the top 10 of these most visited cities.
    '''

st.divider()

'''
Use the sliders below to adjust the time frames, click the cities on the right to hide them and have a closer look at how precipitation patterns changed across time for different cities.
'''

st.divider()

col1, col2, col3 = st.columns([10,1,10])

with col1:
    query = f'''
            SELECT 
                strftime("%Y", date) AS year,
                SUM(precipitation_hours) AS precipitation_hours,
                city
            FROM 
                weather
            GROUP BY 
                year,
                city;
    '''

    df = pd.read_sql(query, engine)
    df['year'] = pd.to_datetime(df['year'])

    # Creating Plotly figure
    fig_1 = px.line(df, x='year', y='precipitation_hours', color='city',
                    title='Yearly Precipitation Hours Across 20 Cities (1940-2024)',
                    labels={'precipitation_hours': 'Total Precipitation Hours', 'year': 'Year', 'city': 'City'})

    # Adding a range slider for year selection
    fig_1.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

    st.plotly_chart(fig_1)

with col3:
    query = f'''
            SELECT 
                strftime("%Y", date) AS year,
                SUM(precipitation_sum) AS precipitation_sum,
                city
            FROM 
                weather
            GROUP BY 
                year,
                city;
    '''

    df = pd.read_sql(query, engine)
    df['year'] = pd.to_datetime(df['year'])

    # Creating Plotly figure
    fig_2 = px.line(df, x='year', y='precipitation_sum', color='city',
                    title='Yearly Precipitation Sum Across 20 Cities',
                    labels={'precipitation_sum': 'Total Precipitation (mm)', 'year': 'Year', 'city': 'City'})

    # Adding a range slider for year selection
    fig_2.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

    st.plotly_chart(fig_2)

st.divider()

'''
### Maybe London is just considered rainy compared to the rest of Europe?
'''

st.divider()

col1, col2 = st.columns(2)

with col1:
    '''
    In this graph we can see that London has had very similar historical rainfall to Paris which makes sense given their geographic closeness. However, we see that London still does not top the rankings for rainiest city in Europe.
    '''

with col2:
    st.image('docs/images/european_precipitation_sum.svg')

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.image('docs/images/european_precipitation_hours.svg')

with col2:
    '''
    Finally, while London seems to be one of the rainier cities in terms of precipitation hours in Europe, it still does not stand out as somewhere particularly rainy compared to Milan for example. Perhaps then this idea that London is rainy comes from the fact that it just isn't as sunny as the other European cities and so that is all its remembered for?
    '''

st.divider()

'''
### Conclusions
'''

st.divider()

'''
The question we set out to answer with this project was whether or not London is a rainy city, and while it certainly rains here (often at the most inconvenient times like on the way to class or when you planned to go to the park), it seems its reputation as a rainy city is probably unjustified. Through our research we found that the stereotype of London as a rainy city has became most prominent during the 2000s, but in reality, London's weather patterns in that period were less rainy and more sunny compared to at other points in its history. We also found that out of the top 20 most visited cities worldwide, London does not stand out as a particularly rainy city being only 16th out of 20 in terms of the average amount of rainfall. So maybe its time for us to collectively hang up the notion that London is an outlier in terms of raininess and think about the things that really stand out about this city.
'''