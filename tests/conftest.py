import pandas as pd
import pytest


@pytest.fixture
def sample_raw() -> pd.DataFrame:
    rows = [
        # ordinary
        {"InvoiceNo": "536365", "StockCode": "85123A", "Description": "WHITE HANGING HEART", "Quantity": 6, "InvoiceDate": "12/1/2010 8:26", "UnitPrice": 2.55, "CustomerID": 17850.0, "Country": "United Kingdom"},
        {"InvoiceNo": "536365", "StockCode": "71053", "Description": "WHITE METAL LANTERN", "Quantity": 6, "InvoiceDate": "12/1/2010 8:26", "UnitPrice": 3.39, "CustomerID": 17850.0, "Country": "United Kingdom"},
        {"InvoiceNo": "536366", "StockCode": "22633", "Description": None, "Quantity": 2, "InvoiceDate": "12/2/2010 9:00", "UnitPrice": 1.95, "CustomerID": None, "Country": "France"},
        # cancellation
        {"InvoiceNo": "C536367", "StockCode": "85123A", "Description": "WHITE HANGING HEART", "Quantity": -6, "InvoiceDate": "12/3/2010 10:00", "UnitPrice": 2.55, "CustomerID": 17850.0, "Country": "United Kingdom"},
        # non-positive price
        {"InvoiceNo": "536368", "StockCode": "71053", "Description": "WHITE METAL LANTERN", "Quantity": 1, "InvoiceDate": "12/4/2010 11:00", "UnitPrice": 0, "CustomerID": 12346.0, "Country": "United Kingdom"},
        # invalid date
        {"InvoiceNo": "536369", "StockCode": "22633", "Description": "UNKNOWN", "Quantity": 3, "InvoiceDate": "not-a-date", "UnitPrice": 1.50, "CustomerID": 12346.0, "Country": "Germany"},
        # duplicate exact row
        {"InvoiceNo": "536365", "StockCode": "85123A", "Description": "WHITE HANGING HEART", "Quantity": 6, "InvoiceDate": "12/1/2010 8:26", "UnitPrice": 2.55, "CustomerID": 17850.0, "Country": "United Kingdom"},
    ]
    return pd.DataFrame(rows)


@pytest.fixture
def prepared_sample(sample_raw):
    from src.transformations import prepare_dataset
    prepared, _ = prepare_dataset(sample_raw)
    return prepared
