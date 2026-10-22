"""Data quality and methodology page."""
from __future__ import annotations

import pandas as pd

import streamlit as st

from src.app_cache import load_prepared_dataset
from src.validation import build_quality_report

st.set_page_config(page_title="Data Quality and Methodology", layout="wide")
st.title("Data quality and methodology")
payload = load_prepared_dataset()
prepared = payload["prepared"]
quality = payload["quality"]
metadata = payload["metadata"]

st.subheader("Source and retrieval")
st.write({"source_url": metadata.source_url, "data_url": metadata.data_url, "dataset": metadata.dataset_name, "doi": metadata.dataset_doi, "retrieved_at_utc": metadata.retrieved_at, "row_count": metadata.row_count, "license": metadata.license_name})

st.subheader("Data-quality counts")
qd = quality.to_dict()
st.dataframe(pd.DataFrame({"metric": list(qd.keys()), "value": list(qd.values())}), use_container_width=True)

st.subheader("Row classification")
st.write("ordinary_sale_rows + exception_rows = total loaded rows")
st.write(f"{quality.ordinary_sale_rows} + {quality.exception_rows} = {quality.total_rows}")

st.subheader("KPI and metric governance")
st.markdown(
    """
    - Sales value (filtered): sum of Quantity × UnitPrice for ordinary sale rows only.
    - Orders / invoices: distinct non-cancellation InvoiceNo among ordinary sale rows.
    - Units sold: sum of positive Quantity over ordinary sale rows.
    - Average order value: sales value ÷ distinct eligible invoices; undefined when no invoices.
    - Active customers: distinct non-null CustomerID among ordinary sale rows.
    - Repeat customers: customers with at least two distinct eligible invoices.
    - RFM recency is measured as of one day after the dataset maximum timestamp.
    - Product ranking groups by StockCode; Description is display only.
    - Currency: GBP (£). No profit, margin, discount, or net revenue claims are made.
    """
)

st.subheader("Dataset limitations")
st.markdown(
    """
    - Historical data: covers December 2010 – December 2011. Not live or current.
    - Cancelled/return lines are reported separately, not automatically netted.
    - Missing CustomerID values mean customer metrics describe a subset of transactions.
    - No cost, discount, or gross margin fields; profit analysis is out of scope.
    - Hosted on a free tier; app may sleep after inactivity.
    """
)
st.write(f"Source citation: {metadata.citation}")
