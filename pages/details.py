import streamlit as st
import pandas as pd
import geopandas as gpd
from collections import Counter
import matplotlib.pyplot as plt

@st.cache_resource
def load_map(shx_file):
    def set_color(x):

        affected = ['ADANA', 'ADIYAMAN', 'DIYARBAKIR', 'SANLIURFA', 'KILIS', 'OSMANIYE', 'ELAZIG']
        extreme = ['KAHRAMANMARAS', 'HATAY']
        if x in affected:
            return 10
        if x in extreme:
            return 20
        else:
            return 8

    map_df = gpd.read_file(shx_file)
    map_df['count'] = map_df['adm1_en'].apply(set_color)
    return map_df


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
# Türkiye | Glide ID EQ-2023-000015-TUR
This is a proof of concept to see what is possible by leveraging secondary data sources from reliefweb.
""")
desc_text = """Type in a date in YYYY-MM-DD format. This will serve as the simulated present."
         In other words, if you type in 2023-08-01, this app will behave as if that is today's
         date and all results will appear as such."""

shx_file = "data//tur_polbnda_adm1.shx"
map_df = load_map(shx_file)
map_df.set_crs("EPSG:4326", inplace=True)
#map_df.plot(figsize=(20, 10))
#st.pyplot(map_df)

plt.figure(figsize=(10, 5))
#map_df.plot(color='slategrey', ax=plt.gca())
map_df.plot(column='count', cmap='Reds', ax=plt.gca())
plt.axis('off')

col1, col2 = st.columns(2)
with col1:
    st.pyplot(plt)

#x.set_axis_off()



#st.pyplot(map_df.plot(cmap='seismic_r', figsize=(20, 10)))
with col2:
    date_of_reference = st.text_input(f"Date of Reference: {desc_text}", '2023-12-10')

#uploaded_file = st.file_uploader("Upload a situation_report preprocessed file")

#if uploaded_file:
    #st.write(f"Filename: {uploaded_file}")
    #df_full = pd.read_excel(uploaded_file)
#    df_full = load_data(uploaded_file)
#else:
df_full = load_data("data//situation_reports.xlsx")







df = df_full[df_full['reported_date'] <= date_of_reference]

st.write("Below is a random sampling of 2 df rows so you can see what columns are in the data.")
st.dataframe(df_full.sample(2),use_container_width=True)

st.subheader("Indicator Selector: Filter statements to your preferred topic area")
st.write("Each indicator has a set of keywords (TODO: Expose these for transparency) "
         "select one and you'll see statements related to that area.")
indicators = get_indicator_columns(df)
ind_opt = st.selectbox('indicator_selector', indicators)
st.write("Here are the top 20 most recent statements ", ind_opt)

df_show = df[df[ind_opt] == 1]
st.dataframe(df_show[['reported_date','identified_adm_chain','spacy_sent_no_paren','authoring_org','source_url']].sort_values(by='reported_date', ascending=False))

