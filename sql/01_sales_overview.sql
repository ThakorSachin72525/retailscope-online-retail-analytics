-- Core sales overview from the normalized in-memory retail view.
-- Filters can be added with WHERE clauses; examples are shown commented.
SELECT
    DATE_TRUNC('month', invoice_date) AS month_start,
    COUNT(DISTINCT invoice_no)       AS eligible_invoices,
    SUM(quantity)                   AS units_sold,
    ROUND(SUM(quantity * unit_price), 2) AS sales_value_gbp
FROM retail
WHERE is_ordinary_sale
--   AND invoice_date BETWEEN DATE '2011-01-01' AND DATE '2011-12-31'
--   AND country = 'United Kingdom'
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY month_start;
