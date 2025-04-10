import pandas as pd
import streamlit as st


def set_base_layout(page_title: str):
    st.set_page_config(
        page_title=page_title,
        layout="wide",
    )

    st.title(page_title)
    st.markdown("---")

    # Sidebar Navigation
    with st.sidebar:
        st.header("Navigation")
        st.page_link("Home.py", label="🏠 Overview")
        st.page_link("pages/1.py", label="📊 Profit Margin Analysis")
        st.page_link("pages/2.py", label="📈 Sales Performance")
        st.page_link("pages/3.py", label="🚢 Shipment Type Segmentation")
        st.page_link("pages/4.py", label="🇺🇸 Geographic Sales Insights")

        st.markdown("---")

        st.markdown(
            """
            This interactive dashboard offers key management insights into **Profit Margins**, **Sales Performance**, and further KPIs.
            """
        )
        st.markdown(
            """
            The dataset, Superstore Sales, contains detailed transactional data from a fictional retail store, including customer information, product categories, sales, profits, and shipping details. The objective was to extract meaningful insights that can be directly applied to improve sales management and strategic decision-making.
            """
        )

        st.caption(
            """
            Developed by *Philipp Meyer & Ole Schildt* as part of the **DS Data Management Fundamentals** course, taught by *Prof. Dr. Giacomo Welsch*.
            """
        )


# Load the dataset DUMMY
def load_data():
    try:
        df = pd.read_csv(".local/data/Superstore.csv")
        print("Dataset loaded successfully!")
        print(f"Number of rows: {df.shape[0]}")
        print(f"Number of columns: {df.shape[1]}")
    except FileNotFoundError:
        print(
            "Error: The specified file was not found. Please check the file path."
        )
        exit()

    df = df.drop(
        [
            "Row ID",
            "Customer ID",
            "Customer Name",
        ],
        axis=1,
    )

    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y")

    df["month"] = df["Order Date"].dt.month
    df["year"] = df["Order Date"].dt.year
    df["year_month"] = df["Order Date"].dt.to_period("M")
    df["total_discount_in_dollars"] = df["Sales"] * df["Discount"]
    df["selling_price"] = df["Sales"] / df["Quantity"]
    df["(net)_profit_before_discount"] = (
        df["Sales"] * df["Discount"] + df["Profit"]
    )
    df["order_fulfillment_time"] = df["Ship Date"] - df["Order Date"]
    df["net_profit_per_unit_sold"] = df["Profit"] / df["Quantity"]
    df = df.rename(columns={"Profit": "net_profit"})
    df["profit_margin"] = df["net_profit"] / df["Sales"] * 100
    df["discounted_sales"] = df["Sales"] - (df["Discount"] * df["Sales"])

    return df


# Create profit_margin_df
def create_profit_margin_df(df):
    profit_margin_df = pd.DataFrame(
        df.groupby(["year", "Category", "Sub-Category"])[
            "profit_margin"
        ].mean()
    ).reset_index()

    return profit_margin_df


def create_sales_performance_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares a DataFrame grouped by year_month with total sales,
    optionally usable for line chart visualizations.
    """
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["year_month"] = df["Order Date"].dt.to_period("M")
    return df
