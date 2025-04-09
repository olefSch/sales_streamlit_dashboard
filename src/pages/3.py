import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.utils import set_base_layout

set_base_layout(page_title="🚢 Shipment Type Segmentation")

st.write("Hi")

df = pd.DataFrame()

# Get unique years and categories for the filters
unique_years = sorted(df["year"].unique())
unique_categories = df["Category"].unique()

# Create sidebar filters
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox(
    "Select Year", ["All"] + list(unique_years)
)
selected_category = st.sidebar.selectbox(
    "Select Category", ["All"] + list(unique_categories)
)

# Filter the DataFrame based on user selections
filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["year"] == selected_year]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# Group by Ship Mode and sum Sales for the donut chart
sales_by_ship_mode = (
    filtered_df.groupby("Ship Mode")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

# Create the donut chart using Plotly
fig = go.Figure(
    data=[
        go.Pie(
            labels=sales_by_ship_mode.index,
            values=sales_by_ship_mode.values,
            hole=0.3,
        )
    ]
)  # Adjust 'hole' for donut size

fig.update_layout(
    title_text=f"Sales Distribution by Shipment Type (Year: {selected_year}, Category: {selected_category})"
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)
