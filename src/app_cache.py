"""Streamlit-aware cached data loading."""
from __future__ import annotations

import streamlit as st

from .config import CACHE_TTL_SECONDS
from .data_source import fetch_online_retail_raw
from .transformations import prepare_dataset
from .validation import build_quality_report, coerce_source_types as _  # noqa: F401


@st.cache_data(show_spinner="Loading the public UCI Online Retail dataset...", ttl=CACHE_TTL_SECONDS)
def load_prepared_dataset() -> dict:
    """Load, validate, classify, and cache the prepared dataset."""
    raw, metadata = fetch_online_retail_raw()
    prepared, conversion_counts = prepare_dataset(raw)
    # Re-validate required columns against the raw input.
    from .validation import validate_required_columns

    validate_required_columns(raw)
    from .validation import build_quality_report as _bqr

    quality = _bqr(raw, prepared, conversion_counts)
    return {
        "raw": raw,
        "prepared": prepared,
        "quality": quality,
        "metadata": metadata,
        "conversion_counts": conversion_counts,
    }


def clear_cache() -> None:
    load_prepared_dataset.clear()
