import streamlit as st

from utils.utils import create_profit_margin_df, load_data, set_base_layout

set_base_layout(page_title="📊 Profit Margin Analysis")

profit_margin_df = create_profit_margin_df(load_data())

st.title("Profit Margin by Sub-Category")

col1, col2 = st.columns(2)

with col1:
    selected_years = st.multiselect(
        "Select Year(s)",
        options=sorted(profit_margin_df["year"].unique()),
        default=sorted(profit_margin_df["year"].unique()),
    )

with col2:
    selected_categories = st.multiselect(
        "Select Category(ies)",
        options=sorted(profit_margin_df["Category"].unique()),
        default=sorted(profit_margin_df["Category"].unique()),
    )

# Filter the dataframe
filtered_df = profit_margin_df[
    (profit_margin_df["year"].isin(selected_years))
    & (profit_margin_df["Category"].isin(selected_categories))
]

# Group by Sub-Category and calculate average profit_margin
grouped = (
    filtered_df.groupby("Sub-Category")["profit_margin"].mean().reset_index()
)
grouped.set_index("Sub-Category", inplace=True)

colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A8"]

# Show chart
st.bar_chart(grouped, horizontal=True)
