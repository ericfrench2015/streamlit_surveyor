import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt


#st.set_page_config(layout="wide")
st.write("""
# Disaster Monitor
This is a proof of concept to see what is possible by leveraging secondary data sources from reliefweb.
""")

uploaded_file = st.file_uploader("Upload a summary file")

if uploaded_file:
    #st.write(f"Filename: {uploaded_file}")
    df = pd.read_excel(uploaded_file)

    #df['identified_country'] = df['identified_country'].astype(str)
    #df['reference_date_iso'] = pd.to_datetime(df['reference_date_iso'])

    countries = Counter(df['identified_country'].tolist())
    st.write("Top 10 countries by reference count in uploaded file")
    df_c = pd.DataFrame(countries.most_common(10), columns=['country','reference_count'])
    st.write(df_c)

    desc_text = """Type in a date in YYYY-MM-DD format. This will serve as the simulated present."
             In other words, if you type in 2023-08-01, this app will behave as if that is today's
             date and all results will appear as such."""
    date_of_reference = st.text_input(f"Date of Reference: {desc_text}")




    countries = Counter(df['identified_country'][df['reference_date_iso'] < date_of_reference].tolist())
    st.write(f"Top 10 countries by reference count in uploaded file given the reference date of {date_of_reference}")
    df_c = pd.DataFrame(countries.most_common(10), columns=['country','reference_count'])
    st.write(df_c)

    #df['max_count'] = df.groupby('identified_country')['num_killed_int'].expanding().max().reset_index(level=0, drop=True)

    df = df[(df['identified_country'] == 'Türkiye')]
    df = df.sort_values(by='reference_date_iso')

    df['max_count'] = df.groupby('identified_country')['num_killed_int'].expanding().max().reset_index(level=0,
                                                                                                       drop=True)
    df['max_count'] = df['max_count'].fillna(0)
    df = df.dropna(subset=['reference_date_iso']).copy()

    plt.figure(figsize=(10, 6))
    df = df.sort_values(by=['identified_country', 'reference_date_iso'])
    for country, data in df.groupby('identified_country'):
        # print(data['reference_date_iso'], data['reference_date_iso'])
        plt.plot(data['reference_date_iso'], data['max_count'], label=country)

    plt.xlabel('Date')
    plt.ylabel('Max Count')
    plt.title('Max Counts by Country over Time (Max from Prior or Current Period)')
    plt.legend()
    plt.grid(False)



    st.pyplot(plt)