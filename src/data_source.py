"""Source retrieval for the UCI Online Retail dataset."""
from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Tuple

import pandas as pd

from .config import (
    DATASET_CITATION,
    DATASET_ID,
    DATASET_NAME,
    LICENSE_NAME,
    SOURCE_DOI,
    SOURCE_PAGE_URL,
)
from .exceptions import DataSourceError, SchemaValidationError

UCI_REPOSITORY_URL = "https://archive.ics.uci.edu/dataset/352/online%2Bretail"


@dataclass(frozen=True)
class SourceMetadata:
    dataset_name: str
    source_url: str
    data_url: str | None
    dataset_doi: str | None
    license_name: str
    citation: str
    retrieved_at: str
    row_count: int


def _fetch_with_retries(max_attempts: int = 2) -> object:
    """Fetch the dataset through ucimlrepo with a bounded retry count."""
    try:
        from ucimlrepo import fetch_ucirepo
    except ImportError as exc:  # pragma: no cover - dependency declared
        raise DataSourceError("ucimlrepo is not installed.") from exc

    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fetch_ucirepo(id=DATASET_ID)
        except Exception as exc:
            last_error = exc
            if attempt < max_attempts:
                time.sleep(min(2 ** (attempt - 1), 4))
    assert last_error is not None
    raise DataSourceError(
        "Unable to retrieve the UCI Online Retail dataset. "
        f"Last error: {last_error}. Source: {SOURCE_PAGE_URL}"
    ) from last_error


def fetch_online_retail_raw() -> tuple[pd.DataFrame, SourceMetadata]:
    """Return the raw UCI Online Retail dataframe and source metadata."""
    dataset = _fetch_with_retries()
    data = getattr(dataset, "data", None)
    raw_frame = getattr(data, "original", None) if data is not None else None
    if not isinstance(raw_frame, pd.DataFrame):
        raise SchemaValidationError("The UCI response did not contain a DataFrame.")

    metadata_blob = getattr(dataset, "metadata", {}) or {}
    if isinstance(metadata_blob, dict):
        meta = metadata_blob
    else:
        meta = getattr(metadata_blob, "__dict__", {}) or {}

    frame = raw_frame.copy()
    missing = [c for c in ("InvoiceNo", "StockCode", "InvoiceDate") if c not in frame.columns]
    if missing:
        raise SchemaValidationError(f"Required source columns are missing: {missing}")

    source_url = meta.get("repository_url") or SOURCE_PAGE_URL
    source_meta = SourceMetadata(
        dataset_name=meta.get("name", DATASET_NAME),
        source_url=source_url,
        data_url=meta.get("data_url"),
        dataset_doi=meta.get("dataset_doi", SOURCE_DOI),
        license_name=LICENSE_NAME,
        citation=meta.get("citation") or DATASET_CITATION,
        retrieved_at=datetime.now(timezone.utc).isoformat(),
        row_count=len(frame),
    )
    return frame, source_meta
