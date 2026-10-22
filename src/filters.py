"""Shared Streamlit filter helpers."""
from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st


def sidebar_filters(prepared: pd.DataFrame, key_prefix: str = "") -> dict[str, Any]:
    ordinary = prepared.loc[prepared["is_ordinary_sale"]] if "is_ordinary_sale" in prepared.columns else prepared
    if ordinary.empty:
        return {"start": None, "end": None, "countries": [], "customer_availability": "all", "top_n": 10}

    min_date = pd.Timestamp(ordinary["InvoiceDate"].min()).date()
    max_date = pd.Timestamp(ordinary["InvoiceDate"].max()).date()

    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key=f"{key_prefix}date_range",
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
    else:
        start, end = min_date, max_date

    countries = sorted(ordinary["Country"].dropna().astype(str).unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Country",
        options=countries,
        default=[],
        key=f"{key_prefix}countries",
    )

    cust_option = st.sidebar.selectbox(
        "Customer ID availability",
        options=["All rows", "Identified customers only", "Unknown customers only"],
        key=f"{key_prefix}cust_availability",
    )
    mapping = {
        "All rows": "all",
        "Identified customers only": "identified",
        "Unknown customers only": "unknown",
    }

    top_n = st.sidebar.slider("Top N", min_value=5, max_value=25, value=10, key=f"{key_prefix}top_n")
    if st.sidebar.button("Reset filters", key=f"{key_prefix}reset"):
        st.rerun()

    return {
        "start": start,
        "end": end,
        "countries": selected_countries,
        "customer_availability": mapping[cust_option],
        "top_n": top_n,
    }
