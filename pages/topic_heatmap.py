import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


@st.cache_resource
def load_joint_sent_and_location():
    df_id_loc = pd.read_excel("data//identified_locations.xlsx")
    df_situation = pd.read_excel("data//situation_reports.xlsx")

    df_situation = df_situation.merge(right=df_id_loc, how='left', left_on='guid_sent', right_on='guid_sent')



    return df_situation



st.header("Topic Matrix over time and by location")
st.write("note this mixes Turkiye and Syrian Locations for now")


df_situation = load_joint_sent_and_location()
df_situation = df_situation.rename(columns={'identified_adm_01_y':'identified_adm_01'})


cols = ['spacy_para_no_paren','reported_date','identified_adm_01','i_killed', 'i_injured', 'i_damage', 'i_infrastructure', 'i_wash', 'i_shelter', 'i_food', 'i_logistic',	'i_health', 'i_gender_pss', 'i_protection']
chart_columns = ['i_killed', 'i_injured', 'i_damage', 'i_infrastructure', 'i_wash', 'i_shelter', 'i_food', 'i_logistic',	'i_health', 'i_gender_pss', 'i_protection']

df_heatmap_reference = df_situation[cols].copy()

from_date = st.text_input(f"From: ", '2023-01-01')
to_date = st.text_input(f"To: ", '2023-12-31')
search_string = st.text_input(f"arbitrary search string: ", '')

df_heatmap = df_heatmap_reference[(df_heatmap_reference['reported_date'] >= from_date) & \
    (df_heatmap_reference['reported_date'] <= to_date)]

df_heatmap['spacy_para_no_paren'].fillna('', inplace=True)

if search_string != '':
    df_heatmap = df_heatmap[df_heatmap['spacy_para_no_paren'].str.contains(search_string)]


df_heatmap = df_heatmap[cols].groupby('identified_adm_01').sum().reset_index()
df_heatmap = df_heatmap[df_heatmap['identified_adm_01'] != 'Turkey or Syria']
df_heatmap = df_heatmap[df_heatmap['i_shelter'] != 0]
df_heatmap.set_index('identified_adm_01', inplace=True)

plt.figure(figsize=(10, 8))  # Adjust the figure size as needed

# Create the heatmap
heatmap = plt.pcolor(df_heatmap[['i_killed', 'i_injured', 'i_damage', 'i_infrastructure', 'i_wash', 'i_shelter', 'i_food', 'i_logistic',	'i_health', 'i_gender_pss', 'i_protection']], cmap='YlGnBu', edgecolors='w', linewidths=1)

# Set the ticks in the middle of the cells
plt.xticks(range(len(df_heatmap.columns)), df_heatmap.columns, rotation=90)
plt.yticks(range(len(df_heatmap.index)), df_heatmap.index)

# Add color bar
plt.colorbar(heatmap)

# Set title and labels
plt.title('Heatmap of Summed Values by identified_adm_01')
plt.xlabel('Columns')
plt.ylabel('identified_adm_01')

# Show the plot
plt.tight_layout()
st.pyplot(plt)


location = st.text_input(f"location: ", 'Aleppo')
topic = st.text_input(f"topic: ", 'i_wash')

df_content = df_heatmap_reference[(df_heatmap_reference['identified_adm_01'] == location) & \
    (df_heatmap_reference[topic] == 1)]

if search_string != '':
    st.dataframe(df_content[df_content['spacy_para_no_paren'].str.contains(search_string)], use_container_width=True)
else:
    st.dataframe(df_content,use_container_width=True)



#st.dataframe(df_heatmap,use_container_width=True)