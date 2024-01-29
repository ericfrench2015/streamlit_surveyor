import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from collections import Counter
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache_resource
def load_joint_sent_and_location():
    df_id_loc = pd.read_excel("data//identified_locations.xlsx")
    df_situation = pd.read_excel("data//situation_reports.xlsx")

    df_situation = df_situation.merge(right=df_id_loc, how='left', left_on='guid_sent', right_on='guid_sent')



    return df_situation




def generate_heatmap(df):
    grouped = df[['glide_id', 'reported_date', 'source_title', 'authoring_org']].drop_duplicates().groupby(
        ['glide_id', 'reported_date', 'authoring_org'])['source_title'].count().reset_index()
    print(grouped.columns)

    pivot_table = grouped.pivot_table(index='authoring_org', columns='reported_date', values='source_title')
    pivot_table = pivot_table.loc[pivot_table.sum(axis=1).sort_values().index]
    pivot_table.fillna(0, inplace=True)

    # Creating the heatmap using Matplotlib
    plt.figure(figsize=(10, 8))
    plt.imshow(pivot_table, cmap='YlGnBu', interpolation='nearest')
    plt.colorbar(label='source_title')
    plt.title('Heatmap of Grouped Data')
    plt.xlabel('Range of Dates')
    plt.ylabel('Authoring Org')

    # Set x and y axis ticks
    #plt.xticks(ticks=range(len(pivot_table.columns)), labels=pivot_table.columns, fontsize=8, rotation=90)
    plt.yticks(ticks=range(len(pivot_table.index)), labels=pivot_table.index, fontsize=8)

    st.pyplot(plt)




st.header("Authoring Organizations over Time")
st.write("See what authors are contributing and when")






## load data
df_situation = load_joint_sent_and_location()
df_heatmap_reference = df_situation.rename(columns={'identified_adm_01_y':'identified_adm_01'})

col1, col2, col3 = st.columns(3)
with col1:
    authoring_org = st.text_input(f"Authoring Org: ", '')
with col2:
    from_date = st.text_input(f"From: ", '2023-01-01')
with col3:
    to_date = st.text_input(f"To: ", '2023-12-31')

df_situation['reported_date'] = pd.to_datetime(df_situation['reported_date'])
#documents_by_date = df_situation.groupby('reported_date')['source_url'].nunique()





#create a df with missing dates
all_dates = pd.date_range(start=df_situation['reported_date'].min(), end=df_situation['reported_date'].max(), freq='D')
new_df = pd.DataFrame(index=all_dates)

# Step 5: Merge the new DataFrame with the original DataFrame
documents_by_date = pd.merge(new_df, df_situation.groupby('reported_date')['source_url'].nunique(), how='left', left_index=True, right_index=True)
documents_by_date['source_url'].fillna(0, inplace=True)


plt.figure(figsize=(10, 6))
documents_by_date.plot(kind='line')
plt.title('Count of Situation Reports Published by Date (all authors)')
#plt.xticks(fontsize=3, rotation=90)
plt.yticks(fontsize=3)
plt.xlabel('Date', fontsize=8)
plt.ylabel('Count of Published Reports')


col1, col2 = st.columns(2)

with col1:
    st.pyplot(plt)



df_heatmap = df_heatmap_reference[(df_heatmap_reference['reported_date'] >= from_date) & \
    (df_heatmap_reference['reported_date'] <= to_date)]

if authoring_org != '':
    df_heatmap = df_heatmap[df_heatmap['authoring_org'] == authoring_org]


with col2:
    ## generate the heatmap
    generate_heatmap(df_heatmap)


#st.dataframe(df_heatmap[['reported_date','authoring_org','source_title']].drop_duplicates(),use_container_width=True)



# Displaying the DataFrame in Streamlit
st.dataframe(df_heatmap[['reported_date','authoring_org','source_title','reference_url']].drop_duplicates(),
    column_config = {
        "reference_url": st.column_config.LinkColumn(
            "URL to source",
            validate="^https://",
            max_chars=100,
        )}
)