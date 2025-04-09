import pandas as pd
import plotly.express as px
import streamlit as st

from config import COLUMNS_BARPLOT
from loader import DataLoader
from utils.utils import set_base_layout

set_base_layout(page_title="📊 Profit Margin Analysis")

loader = DataLoader()


def load_data(loader: DataLoader) -> pd.DataFrame:
    """
    Prepares the DataFrame by converting date columns to datetime format.
    """
    df = loader.get_data_for_metric(COLUMNS_BARPLOT)

    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
    df["year"] = df["Order Date"].dt.year

    df["profit_margin"] = df["Profit"] / df["Sales"] * 100

    df = pd.DataFrame(
        df.groupby(["year", "Category", "Sub-Category"])["profit_margin"]
        .mean()
        .reset_index()
    )

    return df


profit_margin_df = load_data(loader)
col1, col2 = st.columns(2)

# Replace the multiselect for "Select Year(s)" with a selectbox
with col1:
    selected_year = st.selectbox(
        "Select Year",
        options=sorted(profit_margin_df["year"].unique()),
        index=len(profit_margin_df["year"].unique())
        - 1,  # Default to the last year
    )

with col2:
    selected_categories = st.multiselect(
        "Select Category(ies)",
        options=sorted(profit_margin_df["Category"].unique()),
        default=sorted(profit_margin_df["Category"].unique()),
    )

# Filter the dataframe
filtered_df = profit_margin_df[
    (profit_margin_df["year"] == selected_year)
    & (profit_margin_df["Category"].isin(selected_categories))
]

# Group by Sub-Category and calculate average profit_margin
grouped = (
    filtered_df.groupby(["Sub-Category", "Category"])["profit_margin"]
    .mean()
    .reset_index()
)

# 🔧 Define custom colors for categories
custom_colors = {
    "Office Supplies": "#0068c9",  # Dark blue
    "Technology": "#83c9ff",  # Light blue
    "Furniture": "#ff2a2b",  # Red
}

# 🔧 Define a custom sorting order for both legend and plot
category_order = ["Office Supplies", "Technology", "Furniture"]

# 🔧 Ensure the order of Categories in the dataframe matches the custom order
grouped["Category"] = pd.Categorical(
    grouped["Category"], categories=category_order, ordered=True
)

# Sort grouped data by the custom Category order and Sub-Category
grouped = grouped.sort_values(by=["Category", "Sub-Category"])

# Create a Plotly bar chart with Categories mapped to colors
fig = px.bar(
    grouped,
    x="profit_margin",
    y="Sub-Category",
    orientation="h",  # Horizontal bars
    color="Category",  # Map Categories to different colors
    title="Profit Margin by Sub-Category and Category",
    labels={
        "profit_margin": "Profit Margin (%)",
        "Sub-Category": "Sub-Category",
        "Category": "Category",
    },
    text="profit_margin",  # Add profit margin values as text
    color_discrete_map=custom_colors,  # Apply custom colors
    category_orders={
        "Category": category_order
    },  # Enforce the custom Category order
)

# Customize the text display
fig.update_traces(
    texttemplate="%{text:.2f}%",  # Format text as a percentage with 2 decimals
    textposition="inside",  # Position the text inside the bars
)

# Customize the layout
fig.update_layout(
    xaxis_title="Profit Margin (%)",
    yaxis_title="Sub-Category",
    legend_title="Category",  # Add a legend title for clarity
    height=600,  # Adjust chart height
    width=800,  # Adjust chart width
    legend=dict(traceorder="normal"),  # Enforce the legend order
)

with st.container(border=True):
    st.plotly_chart(fig, use_container_width=True)
