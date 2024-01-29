import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_resource
def load_df():
    df = pd.read_excel("data//key_terms_by_day.xlsx")

    return df

@st.cache_resource
def load_svot():
    df = pd.read_excel("data//situation_reports.xlsx")
    df = df.explode('svot')

    return df



df_keywords = load_df()
df_svot = load_svot()



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

st.header("Identified Subject/Verb/Object Combinations")

df_svot = df_svot.explode('svot')
st.dataframe(df_svot[['reported_date','svot']][(df_svot['svot'] != '[]') & (df_svot['reported_date'] == selected_date)],use_container_width=True)


