# Data Dictionary

| Source field | Type | Role | Notes |
|---|---|---|---|
| InvoiceNo | string | ID | Codes beginning with C indicate cancellation/return. |
| StockCode | string | ID | Stable product key. |
| Description | string | Display label | Missing or inconsistent. |
| Quantity | integer | Measure | Positive for ordinary sales candidates. |
| InvoiceDate | datetime | Attribute | Parsed as timestamp; invalid values reported. |
| UnitPrice | decimal | Measure | GBP per unit. |
| CustomerID | nullable integer | ID | Missing means customer-level metrics exclude the row. |
| Country | string | Attribute | Group by source label. |

Derived: `is_cancellation_invoice`, `is_ordinary_sale`, `is_exception`, `exception_reason`, `row_line_value`, `year_month`.
