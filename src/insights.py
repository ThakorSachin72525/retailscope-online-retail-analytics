"""Evidence-based insight helpers."""
from __future__ import annotations

from typing import Iterable

import pandas as pd

from .metrics import country_performance, product_performance, sales_value


def build_overview_insights(filtered: pd.DataFrame, min_rows: int = 50) -> list[str]:
    insights: list[str] = []
    if filtered.empty or len(filtered) < min_rows:
        return ["Not enough observations in the current filter to support a robust insight."]

    total = sales_value(filtered)
    products = product_performance(filtered, top_n=1)
    if not products.empty:
        top = products.iloc[0]
        share = float(top["share_of_sales"])
        insights.append(
            f"The leading product ({top['StockCode']}) accounts for {share:.1%} of filtered sales value."
        )

    countries = country_performance(filtered)
    if not countries.empty:
        top_country = countries.iloc[0]
        insights.append(
            f"{top_country['Country']} contributes {top_country['share_of_sales']:.1%} of filtered sales value."
        )

    # Monthly peak
    monthly = filtered.copy()
    monthly["period"] = monthly["InvoiceDate"].dt.to_period("M")
    monthly["line_value"] = monthly["Quantity"] * monthly["UnitPrice"]
    if not monthly.empty:
        agg = monthly.groupby("period")["line_value"].sum()
        peak_period = agg.idxmax()
        insights.append(f"Peak observed month in the selection: {peak_period} (GBP {agg.max():,.0f}).")

    return insights


def static_methodology_insights() -> list[str]:
    return [
        "Sales value is the sum of Quantity x UnitPrice for ordinary sale rows only; cancellations and exceptions are reported separately.",
        "Customer metrics are based on identifiable CustomerID values only; rows with missing IDs are excluded from customer-level measures but may contribute to sales value.",
        "StockCode is the stable product key because descriptions can be missing or inconsistent.",
        "The underlying dataset covers December 2010 to December 2011 and is historical, not live retail activity.",
    ]
