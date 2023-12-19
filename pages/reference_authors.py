import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_resource
def load_authors():
    df_authors = pd.read_excel("data//authors.xlsx")

    return df_authors


df_authors = load_authors()



st.header("The following authoring organizations and important characteristics"
          "are found below. Source: ReliefWeb API")


selected_authors = st.sidebar.multiselect('Select Org Short Name', df_authors['author_org_short_name'].unique())


filtered_df = df_authors[
    (df_authors['author_org_short_name'].isin(selected_authors))
]

if len(filtered_df) == 0:
    filtered_df = df_authors

#st.dataframe(filtered_df,use_container_width=True)



st.dataframe(filtered_df,use_container_width=True)