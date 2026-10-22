"""Geographic analysis page."""
from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.app_cache import load_prepared_dataset
from src.filters import sidebar_filters
from src.metrics import apply_filters, country_performance

st.set_page_config(page_title="Geographic Analysis", layout="wide")
st.title("Geographic analysis")
st.caption("Countries are compared using the label recorded in the source data.")

payload = load_prepared_dataset()
prepared = payload["prepared"]
filters = sidebar_filters(prepared, key_prefix="geo_")
filtered = apply_filters(prepared, filters["start"], filters["end"], filters["countries"], filters["customer_availability"])

cp = country_performance(filtered)
if cp.empty:
    st.warning("No ordinary sale rows for the selected filters.")
    st.stop()

st.subheader("Country ranking")
st.dataframe(cp, use_container_width=True)

fig = px.bar(cp.head(filters["top_n"]), x="Country", y="sales_value", title="Sales value by country")
fig.update_layout(xaxis_title="Country", yaxis_title="Sales value (GBP)")
st.plotly_chart(fig, use_container_width=True)

fig = px.pie(cp.head(filters["top_n"]), names="Country", values="sales_value", title="Sales share by country")
st.plotly_chart(fig, use_container_width=True)

fig = px.bar(cp.head(filters["top_n"]), x="Country", y="active_customers", title="Identifiable customers by country")
fig.update_layout(xaxis_title="Country", yaxis_title="Identifiable customers")
st.plotly_chart(fig, use_container_width=True)

st.info("The UK is the source retailer base; the Country field records the customer country as captured in the data, not necessarily ship-to logistics facts.")
