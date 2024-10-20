import streamlit as st
import pandas as pd
import numpy as np
from scrape import scrape
import ast

st.title('Remote Job Search')
st.text_input("URL", key="url")
st.text_input("tags", key="tags")
if st.button("Run"):
    with st.spinner('Wait for it...'):
        df = scrape(st.session_state.url)
    st.success("Done!")
    if st.session_state.tags:
        df['tags'] = df['tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        df_filtered = df.explode('tags').reset_index(drop=True)
        if ',' in st.session_state.tags:
            filter_tags = st.session_state.tags.split(',')
        else:
            filter_tags = [st.session_state.tags]
        df_filtered = df_filtered[df_filtered['tags'].isin(filter_tags)]
        if len(df_filtered) > 0:
            st.write(df_filtered)
        else:
            st.error('No job found')
    else:
        st.write(df)