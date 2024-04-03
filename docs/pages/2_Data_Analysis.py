import streamlit as st

st.set_page_config(
    page_title="Data Analysis",
    page_icon="images/RubberDucksLogo.png",
)

# Create header for the webpage with the name of our project and group logo.
# Use two columns to display the logo next to the text.
col1, col2 = st.columns([1, 4])

with col1:
    st.image("images/RubberDucksLogo.png")
with col2:
    st.markdown("<h1 style='font-size: 80px;'>Data Analysis</h1>", unsafe_allow_html=True)