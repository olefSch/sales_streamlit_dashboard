from typing import List, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st

from config import COLUMNS_LINECHART
from loader import DataLoader
from utils.utils import set_base_layout

set_base_layout(page_title="📈 Sales Performance")


def load_data(loader: DataLoader) -> Tuple[pd.DataFrame, List[str]]:
    """
    Prepares the DataFrame by converting date columns to datetime format.
    """
    df = loader.get_data_for_metric(COLUMNS_LINECHART)

    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")

    return df, df["Category"].unique()


df, unique_categories = load_data(DataLoader())

# 🚀 Filters
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    date_range = st.date_input(
        "Select Date Range",
        value=(df["Order Date"].min().date(), df["Order Date"].max().date()),
        min_value=df["Order Date"].min().date(),  # Lock the minimum date
        max_value=df["Order Date"].max().date(),  # Lock the maximum date
    )

with col2:
    granularity = st.selectbox(
        "Select Time Granularity",
        options=["Monthly", "Weekly", "Daily"],
        index=0,
    )

with col3:
    selected_categories = st.multiselect(
        "Select Category(ies)",
        options=list(unique_categories),
        default=list(unique_categories),
    )

# Convert date range
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Apply filters
filtered_df = df[
    (df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)
]

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]

# 🔁 Map granularity to pandas frequency
freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "ME"}

# 🧮 Group by selected frequency and category
sales_over_time = (
    filtered_df.groupby(
        [pd.Grouper(key="Order Date", freq=freq_map[granularity]), "Category"]
    )["Sales"]
    .sum()
    .reset_index()
    .sort_values("Order Date")
)

# 🔧 Define custom colors for categories
custom_colors = {
    "Office Supplies": "#0068c9",  # Dark blue
    "Technology": "#83c9ff",  # Light blue
    "Furniture": "#ff2a2b",  # Red
}

# 🔧 Define a custom legend order
category_order = ["Office Supplies", "Technology", "Furniture"]

# 📈 Plotly line chart
fig = px.line(
    sales_over_time,
    x="Order Date",
    y="Sales",
    color="Category",
    markers=True,
    template="plotly_white",
    title=f"Sales Over Time ({granularity})",
    labels={"Sales": "Total Sales", "Order Date": "Date"},
    color_discrete_map=custom_colors,  # Apply custom colors
    category_orders={
        "Category": category_order
    },  # Enforce custom legend order
)

# Customize layout
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
    title_x=0.5,
    font=dict(family="Arial", size=12, color=st.get_option("theme.textColor")),
)

# 📊 Display the chart
with st.container(border=True):
    st.plotly_chart(fig, use_container_width=True)
