-- Product ranking using StockCode (code) as the stable key.
-- Descriptions are treated as display labels only.
WITH product_sales AS (
    SELECT
        stock_code,
        ANY_VALUE(description)          AS description_label,
        COUNT(DISTINCT invoice_no)      AS invoice_count,
        SUM(quantity)                   AS units_sold,
        ROUND(SUM(quantity * unit_price), 2) AS sales_value_gbp
    FROM retail
    WHERE is_ordinary_sale
    GROUP BY stock_code
),
ranked AS (
    SELECT
        *,
        RANK() OVER (ORDER BY sales_value_gbp DESC) AS sales_rank,
        sales_value_gbp / NULLIF(SUM(sales_value_gbp) OVER (), 0) AS share_of_sales
    FROM product_sales
)
SELECT *
FROM ranked
ORDER BY sales_value_gbp DESC
LIMIT 25;
