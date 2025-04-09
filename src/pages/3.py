import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import COLUMNS_PIECHART
from loader import DataLoader
from utils.utils import set_base_layout

set_base_layout(page_title="🚢 Shipment Type Segmentation")

loader = DataLoader()


def load_data(loader: DataLoader) -> pd.DataFrame:
    """
    Prepares the DataFrame by converting date columns to datetime format.
    """
    df = loader.get_data_for_metric(COLUMNS_PIECHART)

    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y")
    df["Year"] = df["Ship Date"].dt.year

    df = (
        df.groupby(["Year", "Category", "Sub-Category", "Ship Mode"])
        .size()
        .reset_index(name="Shipment Count")
    )

    return df


try:
    shipment_df = load_data(loader)
except Exception as e:
    st.error(f"An error occurred while loading data: {e}")
    st.stop()

# Filter dataset for the selected year
selected_year = st.selectbox(
    "Select Year",
    sorted(shipment_df["Year"].unique()),
    index=len(shipment_df["Year"].unique())
    - 1,  # Default to the most recent year
)

# Filter data by the selected year
filtered_df = shipment_df[shipment_df["Year"] == selected_year]

# Check if there is data after filtering
if filtered_df.empty:
    st.warning(
        "No data available for the selected filters. Please adjust your selections."
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


# Create the plot for all shipments (total distribution)
total_chart = create_pie_chart(filtered_df, "Total Distribution of Ship Modes")

# Create pie charts for each Category
categories = sorted(filtered_df["Category"].unique())
figures = []
for category in categories:
    category_data = filtered_df[filtered_df["Category"] == category]
    if not category_data.empty:
        title = f"Distribution for {category}"
        figures.append(create_pie_chart(category_data, title))

# Add the total chart to the start of the figures list
figures.insert(0, total_chart)

# 2x2 Grid Layout
if len(figures) > 0:
    # First Row
    row1 = st.columns(2)
    row1_figures = figures[:2]  # First two charts
    for i, fig in enumerate(row1_figures):
        with row1[i]:
            st.plotly_chart(fig, use_container_width=True)

    # Second Row
    if len(figures) > 2:
        row2 = st.columns(2)
        row2_figures = figures[2:4]  # Next two charts
        for i, fig in enumerate(row2_figures):
            with row2[i]:
                st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available to display charts.")
