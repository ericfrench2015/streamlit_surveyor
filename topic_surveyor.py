import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import geopandas as gpd


@st.cache_resource
def load_map(shx_file):
    map_df = gpd.read_file(shx_file)
    return map_df

st.set_page_config(layout="wide")


shx_file = "data//tur_polbnda_adm1.shx"
map_df = load_map(shx_file)
#map_df.plot(figsize=(20, 10))
#st.pyplot(map_df)

plt.figure(figsize=(10, 5))
map_df.plot(color='slategrey', ax=plt.gca())
plt.axis('off')




st.write("""
# Disaster Monitor | Türkiye | Glide ID EQ-2023-000015-TUR
This is a proof of concept to see what is possible by leveraging secondary data sources from reliefweb.
""")

#st.write("Instructions: Upload the ongoing.xlsx file here. Note for the POC this will only show Turkiye.")

col1, col2 = st.columns(2)
with col1:
    st.pyplot(plt)

    #uploaded_file = st.file_uploader("Upload a summary file")

with col2:
    desc_text = """Type in a date in YYYY-MM-DD format. This will serve as the simulated present."
                 In other words, if you type in 2023-08-01, this app will behave as if that is today's
                 date and all results will appear as such."""
    date_of_reference = st.text_input(f"Date of Reference: {desc_text}", '2023-12-10')

st.write("testing loading a file from app")
df_full = pd.read_excel("data//ongoing.xlsx")

#st.dataframe(df_test.head(4))

#if uploaded_file:
    #st.write(f"Filename: {uploaded_file}")
#    df_full = pd.read_excel(uploaded_file)




df = df_full[df_full['reference_date_iso'] <= date_of_reference]
col1a, col2a = st.columns(2)
#df['max_count'] = df.groupby('identified_country')['num_killed_int'].expanding().max().reset_index(level=0, drop=True)

df = df[(df['identified_country'] == 'Türkiye') & (df['glide_id'] == 'EQ-2023-000015-TUR')]
df = df.sort_values(by='reference_date_iso')

df['max_count'] = df.groupby('identified_country')['num_killed_int'].expanding().max().reset_index(level=0,
                                                                                                   drop=True)
df['max_count'] = df['max_count'].fillna(0)
df = df.dropna(subset=['reference_date_iso']).copy()

plt.figure(figsize=(10, 6))
df = df.sort_values(by=['identified_country', 'reference_date_iso'])
for country, data in df.groupby('identified_country'):
    # print(data['reference_date_iso'], data['reference_date_iso'])
    plt.plot(data['reference_date_iso'], data['max_count'], label=f"{country}: killed", color='red')

plt.xlabel('Date')
plt.ylabel('Max Count')
plt.title('Max Reported Number of killed in Türkiye over Time (Max from Prior or Current Period)')
plt.legend()
plt.grid(False)
plt.xticks(rotation=90)

with col1a:
    st.pyplot(plt)


df = df[(df['identified_country'] == 'Türkiye')]
df = df.sort_values(by='reference_date_iso')

df['max_count'] = df.groupby('identified_country')['num_injured_int'].expanding().max().reset_index(level=0,
                                                                                                   drop=True)
df['max_count'] = df['max_count'].fillna(0)
df = df.dropna(subset=['reference_date_iso']).copy()

plt.figure(figsize=(10, 6))
df = df.sort_values(by=['identified_country', 'reference_date_iso'])
for country, data in df.groupby('identified_country'):
    # print(data['reference_date_iso'], data['reference_date_iso'])
    plt.plot(data['reference_date_iso'], data['max_count'], label=f"{country}: injured")

plt.xlabel('Date')
plt.ylabel('Max Count')
plt.title('Max Reported Number Injured in Türkiye Time (Max from Prior or Current Period)')
plt.legend()
plt.grid(False)
plt.xticks(rotation=90)
with col2a:
    st.pyplot(plt)

st.subheader("Sorted statements related to number killed")
st.write("pandas df wrapping issue. If you want to see the full content of the source text, right-click,"
         "then left click it.... just go with it")
df_show = df[['reference_date_iso','source_original_text','reference_auth_org']][df['num_killed_int'] > 0]
st.dataframe(df_show.sort_values(by='reference_date_iso', ascending=False),use_container_width=True)