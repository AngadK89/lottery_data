import streamlit as st 
import pandas as pd
from lottery import get_stats

st.header("Hi! Come get your lottery numbers!")

(draw, filtered_results, analysed_results) = get_stats()
no_draw_today = not draw

if no_draw_today:
    st.header("It's a Sunday, take the day off!")
else:
    draw_name = draw.replace("-", " ").title()

st.text("")

if st.button("Get lottery numbers!", disabled=no_draw_today):
    df = pd.read_csv(analysed_results)

    st.header(f"The most frequent balls for {draw_name} are: ")
    df

# Just some basic padding between buttons.
st.markdown("###")

if st.button("Give me all the data!", disabled=no_draw_today):
    st.header(f"Here's all the {draw_name} data for you!")
    filtered_df = pd.read_csv(filtered_results)
    filtered_df



