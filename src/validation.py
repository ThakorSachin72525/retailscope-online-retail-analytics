"""Schema validation and data-quality reporting."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import pandas as pd

from .config import EXPECTED_COLUMNS, REQUIRED_COLUMNS


@dataclass
class QualityReport:
    total_rows: int
    required_columns_present: bool
    missing_required: list[str]
    parsed_rows: int
    invalid_date_rows: int
    cancellation_rows: int
    nonpositive_quantity_rows: int
    nonpositive_price_rows: int
    missing_description_rows: int
    missing_customer_id_rows: int
    exact_duplicate_rows: int
    numeric_conversion_quantity: int
    numeric_conversion_price: int
    ordinary_sale_rows: int
    exception_rows: int
    date_min: str | None
    date_max: str | None
    identified_customer_coverage: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SchemaValidationError(ValueError):
    """Raised for missing or invalid required source fields."""


def validate_required_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise SchemaValidationError(
            "Required source columns are missing or renamed: " + ", ".join(missing)
        )


def coerce_source_types(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Coerce source columns to analysis-friendly types without silently losing issues."""
    out = df.copy()
    qty_before = out["Quantity"].notna().sum() if "Quantity" in out else 0
    price_before = out["UnitPrice"].notna().sum() if "UnitPrice" in out else 0

    out["Quantity"] = pd.to_numeric(out["Quantity"], errors="coerce")
    out["UnitPrice"] = pd.to_numeric(out["UnitPrice"], errors="coerce")

    conversion = {
        "quantity": int(qty_before - out["Quantity"].notna().sum()),
        "price": int(price_before - out["UnitPrice"].notna().sum()),
    }

    if "CustomerID" in out.columns:
        # Convert nullable identifiers to pandas nullable integer type.
        numeric_customer = pd.to_numeric(out["CustomerID"], errors="coerce")
        out["CustomerID"] = numeric_customer.astype("Int64")

    for col in ("InvoiceNo", "StockCode", "Description", "Country"):
        if col in out.columns:
            out[col] = out[col].astype("string").str.strip()

    return out, conversion


def parse_invoice_dates(series: pd.Series) -> pd.Series:
    """Parse UCI retail timestamps robustly; invalid values become NaT.

    The vendored UCI export uses month-first (US-style) dates, while the metadata
    describes the same range in day-first notation. pandas' default inference is
    used deliberately because forcing dayfirst would invalidate more than half of
    the rows.
    """
    return pd.to_datetime(series, errors="coerce")


def count_exact_duplicates(df: pd.DataFrame) -> int:
    return int(df.duplicated(keep=False).sum())


def build_quality_report(
    raw: pd.DataFrame,
    prepared: pd.DataFrame,
    conversion_counts: dict[str, int] | None = None,
) -> QualityReport:
    conversion_counts = conversion_counts or {"quantity": 0, "price": 0}
    parsed_dates = prepared["InvoiceDate"] if "InvoiceDate" in prepared.columns else pd.Series(dtype="datetime64[ns]")
    valid_dates = parsed_dates.notna()

    total = len(prepared)
    cancellation = int(prepared.get("is_cancellation_invoice", pd.Series(dtype=bool)).sum())
    nonpos_qty = int((prepared["Quantity"] <= 0).sum()) if "Quantity" in prepared else 0
    # Simpler: non-positive among numeric converted; missing counts separately.
    nonpos_qty = int(((prepared["Quantity"].notna()) & (prepared["Quantity"] <= 0)).sum()) if "Quantity" in prepared else 0
    nonpos_price = int(((prepared["UnitPrice"].notna()) & (prepared["UnitPrice"] <= 0)).sum()) if "UnitPrice" in prepared else 0

    desc_missing = int(prepared["Description"].isna().sum()) if "Description" in prepared else 0
    if "Description" in prepared:
        desc_missing = int((prepared["Description"].isna() | (prepared["Description"].astype("string").str.strip() == "")).sum())

    cust_missing = int(prepared["CustomerID"].isna().sum()) if "CustomerID" in prepared else 0

    valid_sale_rows = int(prepared.get("is_ordinary_sale", pd.Series(dtype=bool)).sum())
    exception_rows = int(prepared.get("is_exception", pd.Series(dtype=bool)).sum())
    invalid_date_rows = int((~valid_dates).sum())

    date_min = None
    date_max = None
    if valid_dates.any():
        date_min = str(parsed_dates[valid_dates].min().date())
        date_max = str(parsed_dates[valid_dates].max().date())

    identified = int(prepared["CustomerID"].notna().sum()) if "CustomerID" in prepared else 0
    coverage = (identified / total) if total else 0.0

    return QualityReport(
        total_rows=total,
        required_columns_present=all(c in raw.columns for c in REQUIRED_COLUMNS),
        missing_required=[c for c in REQUIRED_COLUMNS if c not in raw.columns],
        parsed_rows=int(valid_dates.sum()),
        invalid_date_rows=invalid_date_rows,
        cancellation_rows=cancellation,
        nonpositive_quantity_rows=nonpos_qty,
        nonpositive_price_rows=nonpos_price,
        missing_description_rows=desc_missing,
        missing_customer_id_rows=cust_missing,
        exact_duplicate_rows=int(raw.duplicated(keep=False).sum()),
        numeric_conversion_quantity=conversion_counts.get("quantity", 0),
        numeric_conversion_price=conversion_counts.get("price", 0),
        ordinary_sale_rows=valid_sale_rows,
        exception_rows=exception_rows,
        date_min=date_min,
        date_max=date_max,
        identified_customer_coverage=coverage,
    )
