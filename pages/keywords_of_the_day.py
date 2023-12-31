import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_resource
def load_df():
    df = pd.read_excel("data//key_terms_by_day.xlsx")

    return df


df_keywords = load_df()



st.header("Most freqent 'noun chunks' by day")


selected_date = st.sidebar.selectbox('Select an end date', df_keywords['reported_date'].unique())


filtered_df = df_keywords[
    (df_keywords['reported_date'] == selected_date) &
    (df_keywords['term_count'] >2)
]

if len(filtered_df) == 0:
    filtered_df = df_keywords

#st.dataframe(filtered_df,use_container_width=True)



st.dataframe(filtered_df,use_container_width=True)