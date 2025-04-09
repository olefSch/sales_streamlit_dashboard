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

# Calculate the maximum profit margin for each Category
category_max_profit = (
    grouped.groupby("Category")["profit_margin"].max().reset_index()
)

# Sort Categories by their maximum profit margin in descending order
category_order = category_max_profit.sort_values(
    by="profit_margin", ascending=False
)["Category"].tolist()

# Sort Sub-Categories within each Category by their profit margin in descending order
sub_category_order = (
    grouped.groupby(["Category", "Sub-Category"])
    .mean()
    .reset_index()
    .sort_values(by=["Category", "profit_margin"], ascending=[False, False])[
        "Sub-Category"
    ]
    .tolist()
)

# Apply the sorted order to the grouped DataFrame
grouped["Category"] = pd.Categorical(
    grouped["Category"], categories=category_order, ordered=True
)
grouped["Sub-Category"] = pd.Categorical(
    grouped["Sub-Category"], categories=sub_category_order, ordered=True
)

# Sort grouped data by Category and Sub-Category
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
    category_orders={
        "Category": category_order,
        "Sub-Category": sub_category_order,
    },
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
)

with st.container(border=True):
    st.plotly_chart(fig, use_container_width=True)
