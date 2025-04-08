import time

import streamlit as st

from utils.utils import set_base_layout

set_base_layout(page_title="🏠 Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("KPI 1")
    st.metric(label="KPI 1", value="100", delta="10", border=True)

with col2:
    st.header("KPI 2")
    st.metric(label="KPI 1", value="100", delta="10", border=True)

with col3:
    st.header("KPI 3")
    st.metric(label="KPI 1", value="100", delta="10", border=True)

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
