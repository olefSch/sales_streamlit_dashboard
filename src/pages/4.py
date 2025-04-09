import json
from urllib.request import urlopen

import pandas as pd
import plotly.express as px
import streamlit as st

from config import COLUMNS_GEOMAP
from loader import DataLoader
from utils.utils import set_base_layout

# Set up the page layout
set_base_layout(page_title="🇺🇸 Geographic Performance Insights")

# Initialize the DataLoader
loader = DataLoader()


def load_data(loader: DataLoader) -> pd.DataFrame:
    """
    Prepares the DataFrame by converting date columns to datetime format.
    """
    df = loader.get_data_for_metric(COLUMNS_GEOMAP)

    # Convert "Order Date" to datetime
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    # Drop rows with invalid "Order Date"
    df = df.dropna(subset=["Order Date"])

    # Extract the year from "Order Date"
    df["Year"] = df["Order Date"].dt.year

    return df, df["Category"].unique()


# Load data
try:
    geo_df, unique_categories = load_data(loader)
except Exception as e:
    st.error(f"An error occurred while loading data: {e}")
    st.stop()

# Year selection
selected_year = st.selectbox(
    "Select Year",
    sorted(geo_df["Year"].unique()),
    index=len(geo_df["Year"].unique()) - 1,
)

# Filter data for the selected year to determine the date range
year_filtered_df = geo_df[geo_df["Year"] == selected_year]
min_date = year_filtered_df["Order Date"].min().date()
max_date = year_filtered_df["Order Date"].max().date()

# Filters using columns
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

with col2:
    performance_metric = st.selectbox(
        "Select Performance Metric",
        options=["Profit", "Sales"],  # Metrics available for selection
        index=0,  # Default to "Profit"
    )

with col3:
    selected_categories = st.multiselect(
        "Select Category(ies)",
        options=list(unique_categories),
        default=list(unique_categories),
    )

# Filter data by year, category, and date
filtered_df = geo_df[
    (geo_df["Year"] == selected_year)
    & (geo_df["Category"].isin(selected_categories))
    & (geo_df["Order Date"].dt.date.between(date_range[0], date_range[1]))
]

# Check if filtered data is empty
if filtered_df.empty:
    st.warning(
        "No data available for the selected filters. Please adjust your selections."
    )
    st.stop()

# Determine aggregation column based on selected metric
aggregation_column = "Sales" if performance_metric == "Sales" else "Profit"
color_label = f"Total {performance_metric} ($)"
map_title_prefix = f"Total {performance_metric}"

# Aggregate data
performance_by_state = (
    filtered_df.groupby("State")[aggregation_column].sum().reset_index()
)
performance_by_state.columns = ["State", f"Total {performance_metric}"]

# Load GeoJSON data for US states
with urlopen(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
) as response:
    us_states = json.load(response)

# Create choropleth map
fig = px.choropleth(
    performance_by_state,
    geojson=us_states,
    locations="State",
    featureidkey="properties.name",
    color=f"Total {performance_metric}",
    color_continuous_scale="viridis",
    scope="usa",
    labels={f"Total {performance_metric}": color_label},
    title=f"{map_title_prefix} by State",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

# Display the map in Streamlit
st.plotly_chart(fig)
