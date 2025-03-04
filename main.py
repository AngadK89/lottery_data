import streamlit as st 
import pandas as pd
from lottery import get_stats

if st.button("Get lottery numbers!"):
    (draw, results) = get_stats()

    if not draw:
        st.header("It's a Sunday, take the day off!")

    else:
        draw_name = draw.replace("-", " ").title()
        df = pd.read_csv(results)

        st.header(f"The most frequent balls for {draw_name} are: ")
        df


