import streamlit as st

logo_path = "docs/images/RubberDucksLogo.png"

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