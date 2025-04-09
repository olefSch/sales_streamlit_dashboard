import pandas as pd
import plotly.express as px
import streamlit as st

from utils.utils import create_sales_performance_df, load_data, set_base_layout

set_base_layout(page_title="📈 Sales Performance")

# Load and prepare data
df = create_sales_performance_df(load_data())
df["Order Date"] = pd.to_datetime(df["Order Date"])
unique_categories = df["Category"].unique()

st.title("Sales Performance Over Time")

# 🚀 Filters
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    selected_categories = st.multiselect(
        "Select Category(ies)",
        options=list(unique_categories),
        default=list(unique_categories),
    )

with col2:
    granularity = st.selectbox(
        "Select Time Granularity",
        options=["Daily", "Weekly", "Monthly"],
        index=0,
    )

with col3:
    date_range = st.date_input(
        "Select Date Range",
        value=(df["Order Date"].min().date(), df["Order Date"].max().date()),
    )

# Convert date range
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# ⚙️ Smoothing options
with st.expander("🔧 Smoothing Options"):
    apply_smoothing = st.checkbox(
        "Apply Moving Average Smoothing", value=False
    )
    window_size = st.slider(
        "Rolling Window Size", min_value=2, max_value=30, value=7
    )

# Apply filters
filtered_df = df[
    (df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)
]

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]

# 🔁 Map granularity to pandas frequency
freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}

# 🧮 Group by selected frequency and category
sales_over_time = (
    filtered_df.groupby(
        [pd.Grouper(key="Order Date", freq=freq_map[granularity]), "Category"]
    )["Sales"]
    .sum()
    .reset_index()
    .sort_values("Order Date")
)

# 📉 Apply smoothing if enabled
if apply_smoothing:
    smoothed_df = (
        sales_over_time.sort_values(["Category", "Order Date"])
        .groupby("Category")
        .apply(
            lambda group: group.assign(
                Sales=group["Sales"]
                .rolling(window=window_size, min_periods=1)
                .mean()
            )
        )
        .reset_index(drop=True)
    )
else:
    smoothed_df = sales_over_time

# 📈 Plotly line chart
fig = px.line(
    smoothed_df,
    x="Order Date",
    y="Sales",
    color="Category",
    markers=True,
    template="plotly_white",
    title=f"Sales Over Time ({granularity}) {'(Smoothed)' if apply_smoothing else ''}",
    labels={"Sales": "Total Sales", "Order Date": "Date"},
)

fig.update_layout(xaxis_title="Date", yaxis_title="Sales")

# Display chart
st.plotly_chart(fig, use_container_width=True)
