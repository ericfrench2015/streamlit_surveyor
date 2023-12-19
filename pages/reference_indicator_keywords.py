import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_resource
def load_authors():
    df_indicators = pd.read_excel("data//indicator_words.xlsx")

    return df_indicators


df_indicators = load_authors()



st.header("The following keywords allocate terms to indicators.")
st.write("This is the first place to look if you're confused about why"
         "a particular sentence is in a given indicator. If something is off,"
         "send me a message.")
st.write("The multi-selects operate as OR")

selected_indicators = st.sidebar.multiselect('Select Indicator', df_indicators['indicator'].unique(), default='i_shelter')
selected_words = st.sidebar.multiselect('Select Word', df_indicators['word'].unique())

filtered_df = df_indicators[
    (df_indicators['indicator'].isin(selected_indicators)) |
    (df_indicators['word'].isin(selected_words))
]

st.dataframe(filtered_df,use_container_width=True)