import pandas as pd
import plotly.express as px
import streamlit as st

from utils.utils import set_base_layout

set_base_layout(page_title="🌍 Geographic Sales Insights")

df = pd.DataFrame()  # Replace with your actual DataFrame


# Assuming your DataFrame is named 'df' and has columns:
# ['Country', 'State', 'City', 'Sales']

# Get unique countries for the filter
unique_countries = df["Country"].unique()

# Create sidebar filter for country
st.sidebar.header("Filter Data")
selected_country = st.sidebar.selectbox(
    "Select Country", ["All"] + list(unique_countries)
)

# Filter the DataFrame based on the selected country
filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

# Group by State and sum Sales for the choropleth map
sales_by_state = filtered_df.groupby("State")["Sales"].sum().reset_index()

# Create the choropleth map using Plotly Express
fig = px.choropleth(
    sales_by_state,
    locations="State",
    locationmode="USA-states",  # Adjust if your data is for a different country
    color="Sales",
    color_continuous_scale="viridis",
    scope="usa",  # Adjust the scope if your data is for a different country
    title=f"Sales by State (Country: {selected_country})",
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)
