"""Central metric and KPI calculations."""
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

from .config import CURRENCY, CURRENCY_SYMBOL


def safe_divide(numerator: float, denominator: float) -> float | None:
    if denominator == 0 or pd.isna(denominator):
        return None
    return float(numerator / denominator)


def apply_filters(
    prepared: pd.DataFrame,
    start_date=None,
    end_date=None,
    countries=None,
    customer_availability: str = "all",
    top_n: int | None = None,
) -> pd.DataFrame:
    """Return ordinary-sale rows matching the requested filters."""
    if "is_ordinary_sale" not in prepared.columns:
        raise ValueError("prepared data must contain row classification columns")
    frame = prepared.loc[prepared["is_ordinary_sale"]].copy()
    if start_date is not None:
        frame = frame.loc[frame["InvoiceDate"] >= pd.Timestamp(start_date, tz=None)]
    if end_date is not None:
        frame = frame.loc[frame["InvoiceDate"] <= pd.Timestamp(end_date, tz=None) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)]
    if countries:
        frame = frame.loc[frame["Country"].isin(list(countries))]
    if customer_availability == "identified":
        frame = frame.loc[frame["CustomerID"].notna()]
    elif customer_availability == "unknown":
        frame = frame.loc[frame["CustomerID"].isna()]
    return frame


def sales_value(frame: pd.DataFrame) -> float:
    return float((frame["Quantity"] * frame["UnitPrice"]).sum()) if not frame.empty else 0.0


def invoice_count(frame: pd.DataFrame) -> int:
    return int(frame["InvoiceNo"].nunique()) if not frame.empty else 0


def units_sold(frame: pd.DataFrame) -> float:
    return float(frame["Quantity"].sum()) if not frame.empty else 0.0


def average_order_value(frame: pd.DataFrame) -> float | None:
    orders = invoice_count(frame)
    if orders == 0:
        return None
    return float(sales_value(frame) / orders)


def active_customers(frame: pd.DataFrame) -> int:
    if frame.empty or "CustomerID" not in frame.columns:
        return 0
    return int(frame["CustomerID"].dropna().nunique())


def repeat_customers(frame: pd.DataFrame) -> int:
    if frame.empty or "CustomerID" not in frame.columns:
        return 0
    customer_invoices = frame.dropna(subset=["CustomerID"]).groupby("CustomerID")["InvoiceNo"].nunique()
    return int((customer_invoices >= 2).sum())


def repeat_customer_share(frame: pd.DataFrame) -> float | None:
    active = active_customers(frame)
    if active == 0:
        return None
    return float(repeat_customers(frame) / active)


def exception_value(frame: pd.DataFrame) -> float:
    from .transformations import exception_value_series

    s = exception_value_series(frame)
    return float(s.sum())


def kpi_bundle(frame: pd.DataFrame) -> dict[str, object]:
    sv = sales_value(frame)
    orders = invoice_count(frame)
    return {
        "sales_value": sv,
        "invoice_count": orders,
        "units_sold": units_sold(frame),
        "average_order_value": average_order_value(frame),
        "active_customers": active_customers(frame),
        "repeat_customers": repeat_customers(frame),
        "repeat_customer_share": repeat_customer_share(frame),
        "currency": CURRENCY,
        "currency_symbol": CURRENCY_SYMBOL,
    }


def _line_sales(d: pd.DataFrame) -> float:
    return float((d["Quantity"] * d["UnitPrice"]).sum())


def monthly_series(prepared_ordinary: pd.DataFrame) -> pd.DataFrame:
    if prepared_ordinary.empty:
        return pd.DataFrame(columns=["period", "sales_value", "invoice_count", "units_sold"])
    out = prepared_ordinary.copy()
    out["period"] = out["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
    records = []
    for period, d in out.groupby("period"):
        records.append({
            "period": period,
            "sales_value": _line_sales(d),
            "invoice_count": d["InvoiceNo"].nunique(),
            "units_sold": float(d["Quantity"].sum()),
        })
    return pd.DataFrame(records).sort_values("period").reset_index(drop=True)


def daily_series(prepared_ordinary: pd.DataFrame) -> pd.DataFrame:
    if prepared_ordinary.empty:
        return pd.DataFrame(columns=["date", "sales_value", "invoice_count", "units_sold"])
    out = prepared_ordinary.copy()
    out["date"] = out["InvoiceDate"].dt.to_period("D").dt.to_timestamp()
    records = []
    for date, d in out.groupby("date"):
        records.append({
            "date": date,
            "sales_value": _line_sales(d),
            "invoice_count": d["InvoiceNo"].nunique(),
            "units_sold": float(d["Quantity"].sum()),
        })
    return pd.DataFrame(records).sort_values("date").reset_index(drop=True)


def product_performance(prepared_ordinary: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    if prepared_ordinary.empty:
        return pd.DataFrame(columns=["StockCode", "description", "sales_value", "units_sold", "invoice_count", "share_of_sales"])
    g = prepared_ordinary.groupby("StockCode", as_index=False, dropna=False).agg(
        units_sold=("Quantity", "sum"),
        invoice_count=("InvoiceNo", "nunique"),
        description=("Description", lambda s: _first_non_null(s)),
    )
    sales_by_product = prepared_ordinary.groupby("StockCode").apply(_line_sales).rename("sales_value")
    g = g.merge(sales_by_product, on="StockCode", how="left")
    total = g["sales_value"].sum() or 1
    g["share_of_sales"] = g["sales_value"] / total
    g = g.sort_values("sales_value", ascending=False).head(top_n).reset_index(drop=True)
    g["description"] = g["description"].fillna("Unknown / missing description")
    return g


def _first_non_null(series: pd.Series):
    s = series.dropna()
    if len(s) == 0:
        return None
    # most common non-null description
    try:
        return s.mode().iloc[0]
    except Exception:
        return s.iloc[0]


def low_activity_products(prepared_ordinary: pd.DataFrame, max_total_units: float = 20, top_n: int = 15) -> pd.DataFrame:
    if prepared_ordinary.empty:
        return pd.DataFrame()
    g = product_performance(prepared_ordinary.assign(_all=1), top_n=10_000)
    # rebuild full, not top
    full = prepared_ordinary.groupby("StockCode", as_index=False, dropna=False).agg(
        units_sold=("Quantity", "sum"),
        invoice_count=("InvoiceNo", "nunique"),
        description=("Description", lambda s: _first_non_null(s)),
    )
    sales_by_product = prepared_ordinary.groupby("StockCode").apply(_line_sales).rename("sales_value")
    full = full.merge(sales_by_product, on="StockCode", how="left")
    full["description"] = full["description"].fillna("Unknown / missing description")
    low = full.loc[full["units_sold"] <= max_total_units].sort_values("sales_value").head(top_n)
    return low.reset_index(drop=True)


def country_performance(prepared_ordinary: pd.DataFrame) -> pd.DataFrame:
    if prepared_ordinary.empty:
        return pd.DataFrame(columns=["Country", "sales_value", "invoice_count", "active_customers", "share_of_sales"])
    g = prepared_ordinary.groupby("Country", as_index=False, dropna=False).agg(
        invoice_count=("InvoiceNo", "nunique"),
        active_customers=("CustomerID", lambda s: s.dropna().nunique()),
    )
    sales_by_country = prepared_ordinary.groupby("Country").apply(_line_sales).rename("sales_value")
    g = g.merge(sales_by_country, on="Country", how="left")
    total = g["sales_value"].sum() or 1
    g["share_of_sales"] = g["sales_value"] / total
    return g.sort_values("sales_value", ascending=False).reset_index(drop=True)


def country_series(prepared_ordinary: pd.DataFrame) -> pd.DataFrame:
    if prepared_ordinary.empty:
        return pd.DataFrame(columns=["period", "Country", "sales_value"])
    out = prepared_ordinary.copy()
    out["period"] = out["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
    records = []
    for (period, country), d in out.groupby(["period", "Country"]):
        records.append({"period": period, "Country": country, "sales_value": _line_sales(d)})
    return pd.DataFrame(records).sort_values(["period", "sales_value"], ascending=[True, False]).reset_index(drop=True)


def rfm_segments(prepared_ordinary: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (customer_rfm dataframe, segment summary)."""
    if prepared_ordinary.empty:
        return pd.DataFrame(), pd.DataFrame()
    snapshot = prepared_ordinary["InvoiceDate"].max() + pd.Timedelta(days=1)
    g = prepared_ordinary.dropna(subset=["CustomerID"]).groupby("CustomerID", as_index=False).agg(
        last_invoice=("InvoiceDate", "max"),
        frequency=("InvoiceNo", "nunique"),
        monetary=("Quantity", lambda s: float((prepared_ordinary.loc[s.index, "Quantity"] * prepared_ordinary.loc[s.index, "UnitPrice"]).sum())),
    )
    g["recency_days"] = (snapshot - g["last_invoice"]).dt.days

    # Quintile scores (1 low, 5 high). Recency is inverted (lower better).
    def qscore(series: pd.Series, reverse: bool = False) -> pd.Series:
        try:
            q = pd.qcut(series.rank(method="first"), 5, labels=[1, 2, 3, 4, 5], duplicates="drop")
        except ValueError:
            q = pd.Series([3] * len(series), index=series.index)
        q = q.astype(int)
        return 6 - q if reverse else q

    g["r_score"] = qscore(g["recency_days"], reverse=True)
    g["f_score"] = qscore(g["frequency"], reverse=False)
    g["m_score"] = qscore(g["monetary"], reverse=False)

    def segment(row) -> str:
        if row["r_score"] >= 4 and row["f_score"] >= 4 and row["m_score"] >= 4:
            return "Champions"
        if row["f_score"] >= 4 and row["m_score"] >= 4:
            return "Loyal"
        if row["r_score"] >= 4 and row["f_score"] >= 2:
            return "Potential loyalists"
        if row["r_score"] <= 2 and row["f_score"] >= 3:
            return "At risk"
        if row["m_score"] >= 4:
            return "Big spenders"
        return "Hibernating / lost"

    g["segment"] = g.apply(segment, axis=1)
    summary = g.groupby("segment", as_index=False).agg(
        customers=("CustomerID", "nunique"),
        avg_recency=("recency_days", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
    ).sort_values("customers", ascending=False)
    return g, summary

