"""Normalization, row classification, and derived analytical fields."""
from __future__ import annotations

import pandas as pd

from .config import EXPECTED_COLUMNS
from .validation import coerce_source_types, parse_invoice_dates


def normalize_raw(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Coerce types and create normalized audit columns. Returns (df, conversion_counts)."""
    df = raw.copy()
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    df, conversion_counts = coerce_source_types(df)
    df["InvoiceDate"] = parse_invoice_dates(df["InvoiceDate"])
    return df, conversion_counts


def classify_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Add documented row classification columns without dropping rows."""
    out = df.copy()

    invoice = out["InvoiceNo"].astype("string").fillna("").str.strip()
    out["is_cancellation_invoice"] = invoice.str.upper().str.startswith("C")

    quantity = pd.to_numeric(out["Quantity"], errors="coerce")
    price = pd.to_numeric(out["UnitPrice"], errors="coerce")
    invalid_quantity = quantity.isna() | (quantity <= 0)
    invalid_price = price.isna() | (price <= 0)
    invalid_date = pd.to_datetime(out["InvoiceDate"], errors="coerce").isna()

    out["is_invalid_date"] = invalid_date
    out["is_nonpositive_quantity"] = quantity.notna() & (quantity <= 0)
    out["is_nonpositive_price"] = price.notna() & (price <= 0)

    # Mutually exclusive reason codes in explicit priority order.
    reason = pd.Series(pd.NA, index=out.index, dtype="string")
    is_cancellation = out["is_cancellation_invoice"].fillna(False).astype(bool)
    reason = reason.mask(is_cancellation, "CANCELLATION")
    reason = reason.mask(reason.isna() & invalid_date, "INVALID_DATE")
    reason = reason.mask(reason.isna() & quantity.isna(), "INVALID_QUANTITY_TYPE")
    reason = reason.mask(reason.isna() & (quantity.notna() & (quantity <= 0)), "NONPOSITIVE_QUANTITY")
    reason = reason.mask(reason.isna() & price.isna(), "INVALID_PRICE_TYPE")
    reason = reason.mask(reason.isna() & (price.notna() & (price <= 0)), "NONPOSITIVE_PRICE")

    out["exception_reason"] = reason
    out["is_exception"] = (
        is_cancellation | invalid_date | quantity.isna() | invalid_quantity | price.isna() | invalid_price
    )
    out["is_ordinary_sale"] = ~out["is_exception"]

    out["row_line_value"] = quantity * price
    out["ordinary_sale_value"] = out["row_line_value"].where(out["is_ordinary_sale"], 0.0)
    # Negative qty impact for exception value computation is handled in metrics.

    out["year_month"] = out["InvoiceDate"].dt.to_period("M").astype("string")
    out["invoice_date_only"] = out["InvoiceDate"].dt.date
    return out


def exception_value_series(df: pd.DataFrame) -> pd.Series:
    """Absolute monetary amount for cancellation/non-positive quantity/price rows."""
    out = df.copy()
    qty = pd.to_numeric(out["Quantity"], errors="coerce")
    price = pd.to_numeric(out["UnitPrice"], errors="coerce")
    valid_amount = qty.notna() & price.notna()
    amount = (qty.abs() * price.abs()).where(valid_amount, 0.0)

    is_cancellation = out["is_cancellation_invoice"].fillna(False).astype(bool)
    nonpos = (
        ((qty.notna() & (qty <= 0)) | (price.notna() & (price <= 0)))
    )
    cancellation_or_nonpos = is_cancellation | nonpos
    # invalid-date-only rows excluded from exception value.
    invalid_date = out["InvoiceDate"].isna() if "InvoiceDate" in out else pd.Series(False, index=out.index)
    # Keep rows that are cancellation/nonpos regardless of date validity.
    mask = cancellation_or_nonpos
    return amount.where(mask, 0.0)



def prepare_dataset(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Normalize, coerce, classify, and return conversion counts."""
    normalized, conversion = normalize_raw(raw)
    prepared = classify_rows(normalized)
    return prepared, conversion
