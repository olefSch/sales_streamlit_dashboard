import time

import pandas as pd
import streamlit as st

from config import COLUMNS_BARPLOT
from loader import DataLoader
from utils.utils import set_base_layout

set_base_layout(page_title="🏠 Overview")

loader = DataLoader()


def load_data(loader: DataLoader) -> pd.DataFrame:
    """
    Prepares the DataFrame by converting date columns to datetime format.
    """
    df = loader.get_data_for_metric(COLUMNS_BARPLOT)

    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
    df["year"] = df["Order Date"].dt.year

    df["profit_margin"] = df["Profit"] / df["Sales"] * 100

    return df


# Load data
data = load_data(loader)

# Filter data for 2014 and 2013
data_2014 = data[data["year"] == 2014]
data_2013 = data[data["year"] == 2013]

# Calculate KPIs for 2014
sales_2014 = data_2014["Sales"].sum()
profit_2014 = data_2014["Profit"].sum()
average_deal_size_2014 = data_2014["Sales"].mean()

# Calculate KPIs for 2013
sales_2013 = data_2013["Sales"].sum()
profit_2013 = data_2013["Profit"].sum()
average_deal_size_2013 = data_2013["Sales"].mean()

# Calculate deltas
sales_delta = sales_2014 - sales_2013
profit_delta = profit_2014 - profit_2013
average_deal_size_delta = average_deal_size_2014 - average_deal_size_2013

# KPI Section
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.metric(
        label="Total Sales (2014)",
        value=f"{sales_2014:,.2f}$",
        delta=f"{sales_delta:,.2f}$ (Prior Year)",
        border=True,
    )

with kpi_col2:
    st.metric(
        label="Total Profit (2014)",
        value=f"{profit_2014:,.2f}$",
        delta=f"{profit_delta:,.2f}$ (Prior Year)",
        border=True,
    )

with kpi_col3:
    st.metric(
        label="Average Deal Size (2014)",
        value=f"{average_deal_size_2014:,.2f}$",
        delta=f"{average_deal_size_delta:,.2f}$ (Prior Year)",
        border=True,
    )

_DUMMY_TEXT = """
✅ 1. Umsatzentwicklung
Der monatliche Umsatz verzeichnete im aktuellen Berichtszeitraum einen Anstieg von 12,4 % im Vergleich zum Vormonat. Besonders stark war die Nachfrage im Bereich digitale Dienstleistungen. Prognosen deuten auf eine stabile Fortsetzung des Wachstumstrends hin.

📦 2. Auftragsstatus & Lieferperformance
Die durchschnittliche Lieferzeit konnte auf 2,3 Werktage reduziert werden. Aktuell befinden sich 86 % der Bestellungen im Status „ausgeliefert“, während 8 % in Bearbeitung sind. Die Pünktlichkeitsquote liegt bei 94,1 %.

👥 3. Kundenzufriedenheit (NPS)
Der Net Promoter Score (NPS) liegt aktuell bei +62, was auf eine hohe Kundenzufriedenheit hinweist. Die Hauptgründe für positive Bewertungen sind Zuverlässigkeit, schneller Support und produktbezogene Innovation.
"""


# Change afterwards for LLM Stream
def stream_data():
    for word in _DUMMY_TEXT.split(" "):
        yield word + " "
        time.sleep(0.02)


with st.container(border=True):
    with st.chat_message("assistant"):
        st.markdown("##### LLM-Description: ")
        st.write_stream(stream_data())
