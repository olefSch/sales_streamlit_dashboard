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
        st.page_link("Home.py", label="🏠 Startseite")
        st.page_link("pages/1.py", label="📊 Profit Margin")
        st.page_link("pages/2.py", label="📈 Sales")
        st.page_link("pages/3.py", label="🚢 Shipment Segmentation")
        st.page_link("pages/4.py", label="🔢 KPIs")
        st.page_link("pages/5.py", label="🌍 Geospacial Analysis")

        st.markdown("---")
        st.caption(
            "WI22A26S - DS Data Management Fundamentals @ Prof. Dr. Giacomo Welsch"
        )
