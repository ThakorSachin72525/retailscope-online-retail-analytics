-- Data-quality audit for the normalized in-memory dataset.
SELECT
    COUNT(*)                                         AS total_rows,
    SUM(CASE WHEN is_cancellation_invoice THEN 1 ELSE 0 END) AS cancellation_rows,
    SUM(CASE WHEN is_invalid_date THEN 1 ELSE 0 END) AS invalid_date_rows,
    SUM(CASE WHEN is_exception THEN 1 ELSE 0 END)    AS exception_rows,
    SUM(CASE WHEN is_ordinary_sale THEN 1 ELSE 0 END) AS ordinary_sale_rows,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_id_rows,
    SUM(CASE WHEN description IS NULL OR TRIM(description) = '' THEN 1 ELSE 0 END) AS missing_description_rows
FROM retail;

-- Distinct duplicate rows (full row) are checked in Python; SQL keeps them visible:
SELECT stock_code, COUNT(*) AS line_count
FROM retail
GROUP BY stock_code
ORDER BY line_count DESC
LIMIT 10;
