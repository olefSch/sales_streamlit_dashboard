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


shipment_df = load_data(loader)

col1, col2 = st.columns(2)

with col1:
    selected_years = st.selectbox(
        "Select Year",
        sorted(shipment_df["Year"].unique()),
    )

with col2:
    selected_categories = st.multiselect(
        "Select Category(ies)",
        options=sorted(shipment_df["Category"].unique()),
        default=sorted(shipment_df["Category"].unique()),
    )

# Filter the dataframe
filtered_df = shipment_df[
    (shipment_df["Year"] == selected_years)
    & (shipment_df["Category"].isin(selected_categories))
]

shipment_counts = (
    filtered_df.groupby("Ship Mode")["Shipment Count"]
    .sum()
    .sort_values(ascending=False)
)

# Create the donut chart using Plotly
fig = go.Figure(
    data=[
        go.Pie(
            labels=shipment_counts.index,
            values=shipment_counts.values,
            hole=0.3,
        )
    ]
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)
