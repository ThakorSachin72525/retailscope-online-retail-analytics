"""Customer analysis page."""
from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.app_cache import load_prepared_dataset
from src.filters import sidebar_filters
from src.metrics import active_customers, apply_filters, repeat_customer_share, repeat_customers, rfm_segments

st.set_page_config(page_title="Customer Analysis", layout="wide")
st.title("Customer analysis")
st.caption("Customer metrics use identifiable CustomerID values only.")

payload = load_prepared_dataset()
prepared = payload["prepared"]
filters = sidebar_filters(prepared, key_prefix="customer_")
filtered = apply_filters(prepared, filters["start"], filters["end"], filters["countries"], filters["customer_availability"])

cust = filtered.dropna(subset=["CustomerID"])
st.metric("Identified customers in selection", f"{active_customers(filtered):,}")
share = repeat_customer_share(filtered)
st.metric("Repeat-customer share", "—" if share is None else f"{share:.1%}")
st.metric("Repeat customers (>=2 invoices)", f"{repeat_customers(filtered):,}")

if filtered.empty:
    st.warning("No ordinary sale rows for the selected filters.")
    st.stop()

# Orders per customer distribution
orders_per_customer = cust.groupby("CustomerID")["InvoiceNo"].nunique()
if not orders_per_customer.empty:
    dist = orders_per_customer.value_counts().sort_index().reset_index()
    dist.columns = ["orders", "customers"]
    fig = px.bar(dist, x="orders", y="customers", title="Orders per identified customer")
    st.plotly_chart(fig, use_container_width=True)

rfm, summary = rfm_segments(filtered)
if not summary.empty:
    st.subheader("RFM segment summary")
    st.dataframe(summary, use_container_width=True)
    fig = px.bar(summary, x="segment", y="customers", title="Customers by RFM segment")
    st.plotly_chart(fig, use_container_width=True)

st.info(
    "Missing CustomerID coverage means customer metrics describe only a subset of all transactions. "
    "No raw customer IDs or transaction histories are displayed."
)
