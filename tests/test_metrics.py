from src.metrics import (
    active_customers,
    apply_filters,
    average_order_value,
    invoice_count,
    product_performance,
    repeat_customers,
    repeat_customer_share,
    sales_value,
    units_sold,
)


def test_hand_built_fixture_kpis(prepared_sample):
    filtered = apply_filters(prepared_sample)
    # 4 ordinary rows, but product grouping. Sales value expected:
    expected = 6 * 2.55 + 6 * 3.39 + 2 * 1.95 + 6 * 2.55
    assert abs(sales_value(filtered) - expected) < 1e-9
    assert invoice_count(filtered) == 2  # 536365 and 536366; duplicate does not add an invoice
    assert units_sold(filtered) == 6 + 6 + 2 + 6
    assert abs(average_order_value(filtered) - (expected / 2)) < 1e-9


def test_missing_customer_not_counted(prepared_sample):
    filtered = apply_filters(prepared_sample)
    # identified active customers: 17850 only? row with missing CustomerID excluded.
    # plus? 536366 missing, so active=1 (17850) because third row missing. duplicate same. yes.
    assert active_customers(filtered) == 1


def test_zero_invoice_period_safe(prepared_sample):
    import pandas as pd
    f = prepared_sample.iloc[0:0].copy()
    fe = apply_filters(f)
    assert average_order_value(fe) is None
    assert repeat_customer_share(fe) is None


def test_date_filter_endpoints(prepared_sample):
    from datetime import date
    f = apply_filters(prepared_sample, start_date=date(2010, 12, 1), end_date=date(2010, 12, 1))
    assert len(f) == 3
    assert sales_value(f) == (6*2.55 + 6*3.39 + 6*2.55)


def test_product_groups_by_stockcode(prepared_sample):
    f = apply_filters(prepared_sample)
    p = product_performance(f, top_n=10)
    # 85123A appears twice stock code, grouped
    row = p.loc[p["StockCode"] == "85123A"].iloc[0]
    assert row["units_sold"] == 12  # 6+6
    assert abs(row["sales_value"] - (6*2.55 + 6*2.55)) < 1e-9


def test_empty_filter_safe(prepared_sample):
    import pandas as pd
    empty_prepared = prepared_sample.iloc[0:0].copy()
    f = apply_filters(empty_prepared)
    assert sales_value(f) == 0
    assert invoice_count(f) == 0
    assert average_order_value(f) is None
    ap = apply_filters(empty_prepared)
    assert product_performance(ap).empty
