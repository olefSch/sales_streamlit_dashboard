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
