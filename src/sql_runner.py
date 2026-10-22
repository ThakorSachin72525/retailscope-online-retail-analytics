"""DuckDB SQL runner for RetailScope."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

SQL_DIR = Path(__file__).resolve().parents[1] / "sql"


def create_view(prepared: pd.DataFrame) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(database=":memory:")
    # Keep original + normalized columns available; add a snake_case view.
    con.register("retail_raw", prepared)
    con.execute(
        """
        CREATE OR REPLACE VIEW retail AS
        SELECT
            "InvoiceNo" AS invoice_no,
            "StockCode" AS stock_code,
            "Description" AS description,
            "Quantity" AS quantity,
            "InvoiceDate" AS invoice_date,
            "UnitPrice" AS unit_price,
            "CustomerID" AS customer_id,
            "Country" AS country,
            "is_cancellation_invoice" AS is_cancellation_invoice,
            "is_invalid_date" AS is_invalid_date,
            "is_exception" AS is_exception,
            "is_ordinary_sale" AS is_ordinary_sale,
            "exception_reason" AS exception_reason,
            "row_line_value" AS row_line_value
        FROM retail_raw
        """
    )
    return con


def run_query(con: duckdb.DuckDBPyConnection, sql: str) -> pd.DataFrame:
    return con.execute(sql).df()


def run_sql_file(con: duckdb.DuckDBPyConnection, path: str | Path) -> pd.DataFrame:
    sql = Path(path).read_text(encoding="utf-8")
    return run_query(con, sql)


def list_sql_files() -> list[Path]:
    if not SQL_DIR.exists():
        return []
    return sorted(SQL_DIR.glob("*.sql"))
