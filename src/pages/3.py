import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import COLUMNS_PIECHART
from loader import DataLoader
from utils.utils import set_base_layout

# Set the base layout for the app
set_base_layout(page_title="🚢 Shipment Type Segmentation")

loader = DataLoader()


def load_data(loader: DataLoader) -> pd.DataFrame:
    """
    Prepares the DataFrame by converting date columns to datetime format.
    """
    df = loader.get_data_for_metric(COLUMNS_PIECHART)

    # Convert ship date to datetime and extract year
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y")
    df["Year"] = df["Ship Date"].dt.year

    # Group the data by relevant columns and count shipments
    df = (
        df.groupby(["Year", "Category", "Sub-Category", "Ship Mode"])
        .size()
        .reset_index(name="Shipment Count")
    )

    return df


# Load data and handle errors
try:
    shipment_df = load_data(loader)
except Exception as e:
    st.error(f"An error occurred while loading data: {e}")
    st.stop()

# 🚀 Filters
col1, col2 = st.columns([1, 2])

# Year selection filter
with col1:
    selected_year = st.selectbox(
        "Select Year",
        sorted(shipment_df["Year"].unique()),  # List of unique years
        index=len(shipment_df["Year"].unique())
        - 1,  # Default to the latest year
    )

# Category selection filter
with col2:
    selected_category = st.selectbox(
        "Select Category",
        sorted(shipment_df["Category"].unique()),  # List of unique categories
        index=0,  # Default to the first category
    )

# Filter data by the selected year and category
filtered_df = shipment_df[
    (shipment_df["Year"] == selected_year)
    & (shipment_df["Category"] == selected_category)
]

# Check if there is data after filtering
if filtered_df.empty:
    st.warning(
        "No data available for the selected year and category. Please adjust your selections."
    )
    st.stop()


# Helper function to create pie chart figures
def create_pie_chart(data: pd.DataFrame, title: str) -> go.Figure:
    shipment_counts = (
        data.groupby("Ship Mode")["Shipment Count"]
        .sum()
        .sort_values(ascending=False)
    )
    fig = go.Figure(
        data=[
            go.Pie(
                labels=shipment_counts.index,
                values=shipment_counts.values,
                hole=0.3,
            )
        ]
    )
    fig.update_layout(title=title, title_x=0.5)
    return fig


# Create the plot for all shipments (total distribution across the selected year)
total_distribution_df = shipment_df[shipment_df["Year"] == selected_year]
total_chart = create_pie_chart(
    total_distribution_df,
    f"Total Distribution of Ship Modes ({selected_year})",
)

# Create the plot for the selected category
category_chart = create_pie_chart(
    filtered_df, f"Distribution for {selected_category}"
)

# 📊 Layout: Display both pie charts in a single row
row = st.columns(2, border=True)

with row[0]:
    st.plotly_chart(total_chart, use_container_width=True)

with row[1]:
    st.plotly_chart(category_chart, use_container_width=True)
