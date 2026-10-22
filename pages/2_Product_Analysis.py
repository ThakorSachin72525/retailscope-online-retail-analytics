"""Product analysis page."""
from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.app_cache import load_prepared_dataset
from src.filters import sidebar_filters
from src.metrics import apply_filters, low_activity_products, product_performance

st.set_page_config(page_title="Product Analysis", layout="wide")
st.title("Product analysis")
st.caption("StockCode is the stable product key; Description is a display label.")

payload = load_prepared_dataset()
prepared = payload["prepared"]
filters = sidebar_filters(prepared, key_prefix="product_")
filtered = apply_filters(prepared, filters["start"], filters["end"], filters["countries"], filters["customer_availability"])

top = product_performance(filtered, top_n=filters["top_n"])
if top.empty:
    st.warning("No ordinary sale rows for the selected filters.")
    st.stop()

st.subheader(f"Top {filters['top_n']} products by sales value")
fig = px.bar(top, x="StockCode", y="sales_value", hover_data=["description", "units_sold", "invoice_count"], title="Product sales value")
fig.update_layout(xaxis_title="StockCode", yaxis_title="Sales value (GBP)")
st.plotly_chart(fig, use_container_width=True)
st.dataframe(top, use_container_width=True)

st.subheader("Top products by units sold")
top_units = product_performance(filtered, top_n=filters["top_n"]).sort_values("units_sold", ascending=False)
fig = px.bar(top_units, x="StockCode", y="units_sold", hover_data=["description"], title="Product units")
fig.update_layout(xaxis_title="StockCode", yaxis_title="Units sold")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Low-activity products")
low = low_activity_products(filtered, max_total_units=50, top_n=filters["top_n"])
if low.empty:
    st.info("No low-activity products for the threshold.")
else:
    st.dataframe(low, use_container_width=True)
    st.caption("Low activity refers to low observed volume/value only. Cost and profit data are not available.")
