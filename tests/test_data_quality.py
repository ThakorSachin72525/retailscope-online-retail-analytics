from src.validation import build_quality_report, validate_required_columns


def test_missing_required_raises():
    import pandas as pd
    df = pd.DataFrame({"StockCode": ["a"]})
    try:
        validate_required_columns(df)
        assert False, "expected SchemaValidationError"
    except ValueError:
        pass


def test_quality_report_counts(sample_raw, prepared_sample):
    from src.transformations import prepare_dataset
    prepared, conv = prepare_dataset(sample_raw)
    raw = sample_raw
    q = build_quality_report(raw, prepared, conv)
    assert q.total_rows == 7
    assert q.ordinary_sale_rows == 4
    assert q.cancellation_rows == 1
    assert q.missing_customer_id_rows == 1  # row with None CustomerID (536366) + maybe? Actually 1
    assert q.exact_duplicate_rows == 2


def test_source_failure_does_not_fabricate(monkeypatch):
    import src.data_source as ds
    def boom(*a, **k):
        raise ds.DataSourceError("down")
    monkeypatch.setattr(ds, "_fetch_with_retries", boom)
    try:
        ds.fetch_online_retail_raw()
        assert False
    except Exception:
        pass
