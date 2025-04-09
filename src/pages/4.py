import json
from urllib.request import urlopen

import plotly.express as px
import streamlit as st

from utils.utils import load_data, set_base_layout

set_base_layout(page_title="🌍 Geographic Performance Insights")

# Load your actual DataFrame here
df = load_data()

# Get unique countries for the filter
unique_countries = df["Country"].unique()

# Create a selectbox above the plot for the country filter
selected_country = st.selectbox(
    "Select Country:", ["All"] + list(unique_countries)
)

# Create radio buttons above the plot for the performance metric filter
performance_metric = st.radio(
    "Select Performance Metric:", ["Sales", "Profit"], horizontal=True
)

# Filter the DataFrame based on the selected country
filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

# Determine the column to aggregate based on the selected metric
if performance_metric == "Sales":
    aggregation_column = "Sales"
    color_label = "Total Sales ($)"
    map_title_prefix = "Total Sales"
else:
    aggregation_column = "Profit"
    color_label = "Total Profit ($)"
    map_title_prefix = "Total Profit"

# Group by State and sum the selected performance metric
performance_by_state = (
    filtered_df.groupby("State")[aggregation_column].sum().reset_index()
)
performance_by_state.columns = ["State", f"Total {performance_metric}"]

# Load GeoJSON for US states
with urlopen(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
) as response:
    us_states = json.load(response)

# Create the choropleth map using Plotly Express
fig = px.choropleth(
    performance_by_state,
    geojson=us_states,
    locations="State",
    featureidkey="properties.name",
    color=f"Total {performance_metric}",
    color_continuous_scale="viridis",
    scope="usa",  # Assuming the selected country is within the USA for state-level mapping
    labels={f"Total {performance_metric}": color_label},
    title=f"{map_title_prefix} by State (Country: {selected_country if selected_country != 'All' else 'All'})",
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)
