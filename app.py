"""RetailScope Streamlit entry point."""
from __future__ import annotations

import streamlit as st

from src.app_cache import load_prepared_dataset
from src.filters import sidebar_filters
from src.insights import build_overview_insights, static_methodology_insights
from src.metrics import (
    active_customers,
    average_order_value,
    country_performance,
    invoice_count,
    kpi_bundle,
    monthly_series,
    product_performance,
    repeat_customer_share,
    sales_value,
    units_sold,
)

st.set_page_config(
    page_title="RetailScope — Online Retail Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("RetailScope — Online Retail Analytics Dashboard")
st.caption(
    "Historical UCI Online Retail analysis (December 2010 – December 2011). "
    "This is a historical dataset, not live sales."
)

try:
    payload = load_prepared_dataset()
except Exception as exc:  # pragma: no cover - UI path
    st.error(
        "The public dataset could not be loaded. Please retry later. "
        "Source: https://archive.ics.uci.edu/dataset/352/online%2Bretail"
    )
    st.exception(exc)
    st.stop()

prepared = payload["prepared"]
metadata = payload["metadata"]
quality = payload["quality"]

filters = sidebar_filters(prepared, key_prefix="home_")
from src.metrics import apply_filters

filtered = apply_filters(
    prepared,
    start_date=filters["start"],
    end_date=filters["end"],
    countries=filters["countries"],
    customer_availability=filters["customer_availability"],
)

st.markdown("### Current selection")
st.write(
    f"Date range: **{filters['start']}** to **{filters['end']}** | "
    f"Countries: {', '.join(filters['countries']) if filters['countries'] else 'All'} | "
    f"Customer scope: {filters['customer_availability']}"
)

kb = kpi_bundle(filtered)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Eligible sales value (GBP)", f"£{kb['sales_value']:,.0f}")
col2.metric("Eligible invoices", f"{kb['invoice_count']:,}")
col3.metric("Units sold", f"{kb['units_sold']:,.0f}")
col4.metric("Identifiable customers", f"{kb['active_customers']:,}")
share = kb["repeat_customer_share"]
col5.metric("Repeat-customer share", "—" if share is None else f"{share:.1%}")

left, right = st.columns(2)
with left:
    st.subheader("Monthly sales trend")
    ms = monthly_series(filtered)
    if ms.empty:
        st.info("No rows for the selected filters.")
    else:
        import plotly.express as px

        fig = px.line(ms, x="period", y="sales_value", markers=True, title="Sales value by month")
        fig.update_layout(xaxis_title="Month", yaxis_title="Sales value (GBP)")
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Country contribution")
    cp = country_performance(filtered).head(filters["top_n"])
    if cp.empty:
        st.info("No rows for the selected filters.")
    else:
        import plotly.express as px

        fig = px.bar(cp, x="Country", y="sales_value", title="Sales value by country")
        fig.update_layout(xaxis_title="Country", yaxis_title="Sales value (GBP)")
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Product leaders")
pp = product_performance(filtered, top_n=filters["top_n"])
if pp.empty:
    st.info("No rows for the selected filters.")
else:
    st.dataframe(pp, use_container_width=True)

st.subheader("Automated insights")
for txt in build_overview_insights(filtered):
    st.write(f"• {txt}")

st.subheader("Methodology and source details")
st.write(f"- Source: {metadata.source_url}")
st.write(f"- Dataset: {metadata.dataset_name} (DOI {metadata.dataset_doi})")
st.write(f"- License: {metadata.license_name}")
st.write(f"- Retrieved at (UTC): {metadata.retrieved_at}")
st.write(f"- Loaded rows: {quality.total_rows:,}; parsed dates: {quality.parsed_rows:,}; ordinary sale rows: {quality.ordinary_sale_rows:,}")
st.write(f"- Date coverage: {quality.date_min} to {quality.date_max}")

with st.expander("Static methodology guidance"):
    for txt in static_methodology_insights():
        st.write(f"• {txt}")
