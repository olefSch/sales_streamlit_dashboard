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
📈 1. Umsatz- und Gewinnentwicklung  
Im Jahr 2014 wurde ein Gesamtumsatz von **733.947,02 \\$** erzielt – ein Plus von **125.473,19 \\$** im Vergleich zum Vorjahr.  
Auch der Gewinn konnte gesteigert werden und lag bei **93.507,51 \\$**, was einer Verbesserung um **11.780,58 \\$** entspricht.  
Diese positive Entwicklung spiegelt die solide Performance des Unternehmens wider.

💰 2. Durchschnittlicher Auftragswert  
Der durchschnittliche Auftragswert betrug im Jahr 2014 **221,13 \\$**.  
Im Vergleich zum Vorjahr bedeutet dies jedoch einen leichten Rückgang von **14,71 \\$**.  
Dies könnte auf kleinere Einzelbestellungen oder veränderte Kaufgewohnheiten hinweisen.

📊 3. Wirtschaftliche Gesamtbewertung  
Trotz des Rückgangs beim durchschnittlichen Auftragswert zeigen die Umsatzzahlen und der gestiegene Gewinn eine robuste Geschäftsentwicklung.  
Die Zahlen legen nahe, dass eine höhere Verkaufsmenge oder effizientere Prozesse zum Erfolg beigetragen haben.
"""


# Change afterwards for LLM Stream
def stream_data():
    for word in _DUMMY_TEXT.split(" "):
        yield word + " "
        time.sleep(0.02)


with st.container(border=True):
    with st.chat_message("assistant"):
        st.markdown("##### Description: ")
        st.write_stream(stream_data())
