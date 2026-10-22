"""Sales trends page."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.app_cache import load_prepared_dataset
from src.filters import sidebar_filters
from src.metrics import apply_filters, daily_series, monthly_series

st.set_page_config(page_title="Sales Trends", layout="wide")
st.title("Sales trends")
st.caption("Historical data — not live sales.")

payload = load_prepared_dataset()
prepared = payload["prepared"]
filters = sidebar_filters(prepared, key_prefix="trends_")
filtered = apply_filters(prepared, filters["start"], filters["end"], filters["countries"], filters["customer_availability"])

monthly = monthly_series(filtered)
daily = daily_series(filtered)

if monthly.empty:
    st.warning("No ordinary sale rows for the selected filters.")
    st.stop()

st.subheader("Monthly sales value")
fig = px.line(monthly, x="period", y="sales_value", markers=True, title="Monthly sales value")
fig.update_layout(xaxis_title="Month", yaxis_title="Sales value (GBP)")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Monthly invoice count and average order value")
monthly["aov"] = monthly["sales_value"] / monthly["invoice_count"].replace(0, pd.NA)

left, right = st.columns(2)
with left:
    fig = px.bar(monthly, x="period", y="invoice_count", title="Invoices per month")
    fig.update_layout(xaxis_title="Month", yaxis_title="Eligible invoices")
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.line(monthly, x="period", y="aov", markers=True, title="Average order value by month")
    fig.update_layout(xaxis_title="Month", yaxis_title="AOV (GBP)")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Daily view")
fig = px.line(daily, x="date", y="sales_value", title="Daily sales value")
fig.update_layout(xaxis_title="Date", yaxis_title="Sales value (GBP)")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(monthly, use_container_width=True)
