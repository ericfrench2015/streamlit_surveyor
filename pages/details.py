import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

@st.cache_resource
def load_data(uploaded_file):
    df_full = pd.read_excel(uploaded_file)
    return df_full

@st.cache_resource
def get_indicator_columns(df):
    inds=[]
    for c in df.columns:
        if c[0:2] == 'i_':
            inds.append(c)

    return inds


st.set_page_config(layout="wide")
st.write("""
# Disaster Monitor Details
This is a proof of concept to see what is possible by leveraging secondary data sources from reliefweb.
""")
desc_text = """Type in a date in YYYY-MM-DD format. This will serve as the simulated present."
         In other words, if you type in 2023-08-01, this app will behave as if that is today's
         date and all results will appear as such."""
date_of_reference = st.text_input(f"Date of Reference: {desc_text}", '2023-12-10')

uploaded_file = st.file_uploader("Upload a situation_report preprocessed file")

if uploaded_file:
    #st.write(f"Filename: {uploaded_file}")
    #df_full = pd.read_excel(uploaded_file)
    df_full = load_data(uploaded_file)


    df = df_full[df_full['reported_date'] <= date_of_reference]

    st.write("Below is a random sampling of 2 df rows so you can see what columns are in the data.")
    st.dataframe(df_full.sample(2),use_container_width=True)

    st.subheader("Indicator Selector: Filter statements to your preferred topic area")
    st.write("Each indicator has a set of keywords (TODO: Expose these for transparency)"
             "select one and you'll see statements related to that area.")
    indicators = get_indicator_columns(df)
    ind_opt = st.selectbox('indicator_selector', indicators)
    st.write("Here are the top 20 most recent statements ", ind_opt)

    df_show = df[df[ind_opt] == 1]
    st.dataframe(df_show[['reported_date','identified_adm_chain','spacy_sent_no_paren','authoring_org','source_url']].sort_values(by='reported_date', ascending=False))

