"""Project configuration and shared constants."""
from __future__ import annotations

DATASET_ID = 352
DATASET_NAME = "UCI Online Retail"
SOURCE_PAGE_URL = "https://archive.ics.uci.edu/dataset/352/online%2Bretail"
SOURCE_DOI = "10.24432/C5BW33"
DATASET_CITATION = (
    "Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. "
    "https://doi.org/10.24432/C5BW33. Licensed under CC BY 4.0."
)
DATASET_DATE_START = "2010-12-01"
DATASET_DATE_END = "2011-12-09"
LICENSE_NAME = "CC BY 4.0 (dataset); project code under MIT License"
CURRENCY = "GBP"
CURRENCY_SYMBOL = "£"
CACHE_TTL_SECONDS = 3600 * 6

REQUIRED_COLUMNS = ["InvoiceNo", "StockCode", "Quantity", "InvoiceDate", "UnitPrice", "Country"]
EXPECTED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]
ID_COLUMNS = ["InvoiceNo", "StockCode", "Country"]
NUMERIC_COLUMNS = ["Quantity", "UnitPrice", "CustomerID"]

ROW_CLASS_RULES = {
    "cancellation": "InvoiceNo begins with C after trimming and case normalization",
    "ordinary_sale": "not cancellation AND Quantity > 0 AND UnitPrice > 0 AND parsed InvoiceDate",
    "exception": "cancellation OR Quantity <= 0 OR UnitPrice <= 0 OR unparseable date",
}
