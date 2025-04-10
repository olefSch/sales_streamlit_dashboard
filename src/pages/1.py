import pandas as pd
import plotly.graph_objects as go
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

# 🔧 Define a custom sorting order for display in the plot (top to bottom)
category_order_plot = ["Furniture", "Technology", "Office Supplies"]

# 🔧 Define a custom sorting order for legend (reversed from plot order)
category_order_legend = ["Office Supplies", "Technology", "Furniture"]

# Sort by profit_margin within each category (descending)
grouped_sorted = pd.DataFrame()
for category in category_order_plot:
    if category in grouped["Category"].values:
        category_data = grouped[grouped["Category"] == category].sort_values(
            by="profit_margin", ascending=True
        )
        grouped_sorted = pd.concat([grouped_sorted, category_data])

# Create an empty figure
fig = go.Figure()

# Manually add traces in reverse order for correct legend display
for category in category_order_legend:
    if category in grouped_sorted["Category"].values:
        cat_data = grouped_sorted[grouped_sorted["Category"] == category]
        fig.add_trace(
            go.Bar(
                x=cat_data["profit_margin"],
                y=cat_data["Sub-Category"],
                name=category,
                orientation="h",
                marker_color=custom_colors[category],
                text=cat_data["profit_margin"],
                texttemplate="%{text:.2f}%",
                textposition="inside",
            )
        )

# Customize the layout
fig.update_layout(
    title="Profit Margin by Sub-Category and Category",
    xaxis_title="Profit Margin (%)",
    yaxis_title="Sub-Category",
    legend_title="Category",
    height=600,
    width=800,
    showlegend=True,
    legend=dict(
        traceorder="reversed"  # This ensures the legend appears in the order traces were added
    ),
    barmode="stack",  # This doesn't affect our horizontal bars but ensures correct legend behavior
)

with st.container(border=True):
    st.plotly_chart(fig, use_container_width=True)
