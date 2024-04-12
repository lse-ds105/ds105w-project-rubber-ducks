import streamlit as st

logo_path = "docs/images/RubberDucksLogo.png"

st.set_page_config(
    page_title="Rubber Ducks Weather Analysis Project",
    page_icon=logo_path,
    layout="wide"
)

# Create header for the webpage with the name of our project and group logo.
# Use two columns to display the logo next to the text.
col1, col2 = st.columns([1, 4])

with col1:
    st.image(logo_path)
with col2:
    st.markdown("<h1 style='font-size: 160px;'>Rubber Ducks</h1>", unsafe_allow_html=True)

"""
## _Is London a rainy city?_
"""

st.image("docs/images/LondonPuddle.JPG")

"""
This is the central question we seek to answer with this project. For many tourists around the world, there is a widely held belief that London is a particularly rainy city where it is unwise to go anywhere without an umbrella or a raincoat and the spectre of a raincloud threatens to ruin any day out you may have planned...but is this actually the case?
"""

st.image("docs/images/LondonSkyline.JPG")

"""
Having spent the last one or two years living in this wonderful city, our group believes that this characterisation is unfair and that London is actually a really great city to visit - especially in the summer when the locals flock to the [Serpentine Lido](https://www.royalparks.org.uk/visit/parks/hyde-park/serpentine-lido) or the [Hampstead Heath Ponds](https://www.hampsteadheath.net/swimming-ponds) to cool off in the hot summer sun.
"""

"""
## Who are we?

- [Oliver Gregory](https://github.com/ollie-gregory) | BSc Economics
- [Noémie Dunand Wisdom](https://github.com/Noemie-DW) | BSc Economics
- [Sofia Giorgianni](https://github.com/sogiorgianni) | LSE General Course
- [Shirley Li](https://github.com/ShirleyL599) | LSE General Course
"""

"""
## Explore our project
"""
col1, col2, col3 = st.columns(3)

with col1:
    c = st.container()
    c.image("docs/images/DataCollection.svg")
    c.markdown("<h3><a href='Data_Collection' style='text-decoration: none;'>Data Collection</a></h3>", unsafe_allow_html=True)
    c.write("Learn about the methods we used to collect and manage our data.")

with col2:
    c = st.container()
    c.image(logo_path)
    c.markdown("<h3><a href='Data_Analysis' style='text-decoration: none;'>Data Analysis</a></h3>", unsafe_allow_html=True)
    c.write("Explore the different ways we visualised the data.")

with col3:
    c = st.container()
    c.image(logo_path)
    c.markdown("<h3><a href='Key_Insights' style='text-decoration: none;'>Key Insights</a></h3>", unsafe_allow_html=True)
    c.write("Understand the key insights of the data and what it means for our project.")