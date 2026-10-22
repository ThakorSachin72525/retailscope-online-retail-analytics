import pandas as pd
from src.sql_runner import create_view, list_sql_files, run_sql_file
from src.transformations import prepare_dataset


def test_sql_files_run(sample_raw):
    prepared, _ = prepare_dataset(sample_raw)
    con = create_view(prepared)
    for path in list_sql_files():
        df = run_sql_file(con, path)
        assert isinstance(df, pd.DataFrame)
    con.close()


def test_sql_rfm(sample_raw):
    prepared, _ = prepare_dataset(sample_raw)
    con = create_view(prepared)
    df = run_sql_file(con, "sql/04_customer_rfm.sql")
    assert "customer_id" in df.columns
    con.close()
