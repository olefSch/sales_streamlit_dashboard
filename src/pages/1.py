import pandas as pd
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
        df.groupby(["year", "Category", "Sub-Category"])[
            "profit_margin"
        ].mean()
    ).reset_index()

    return df


profit_margin_df = load_data(loader)

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
