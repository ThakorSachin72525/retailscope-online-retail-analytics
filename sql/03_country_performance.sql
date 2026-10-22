-- Geographic contribution using the Country label exactly as recorded in the source.
SELECT
    country,
    COUNT(DISTINCT invoice_no)    AS eligible_invoices,
    COUNT(DISTINCT customer_id)    AS identifiable_customers,
    SUM(quantity)                 AS units_sold,
    ROUND(SUM(quantity * unit_price), 2) AS sales_value_gbp,
    ROUND(
        SUM(quantity * unit_price) / NULLIF(SUM(SUM(quantity * unit_price)) OVER (), 0),
        4
    ) AS share_of_filtered_sales
FROM retail
WHERE is_ordinary_sale
GROUP BY country
ORDER BY sales_value_gbp DESC;
