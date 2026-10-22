-- RFM-style snapshot for identifiable customers only.
WITH customer_sales AS (
    SELECT
        customer_id,
        MAX(invoice_date) AS last_invoice_date,
        COUNT(DISTINCT invoice_no) AS frequency,
        SUM(quantity * unit_price) AS monetary_value
    FROM retail
    WHERE is_ordinary_sale
      AND customer_id IS NOT NULL
    GROUP BY customer_id
),
snapshot AS (
    SELECT (MAX(invoice_date) + INTERVAL 1 DAY) AS snapshot_date FROM retail WHERE is_ordinary_sale
)
SELECT
    c.customer_id,
    c.last_invoice_date,
    DATE_DIFF('day', c.last_invoice_date, s.snapshot_date) AS recency_days,
    c.frequency,
    ROUND(c.monetary_value, 2) AS monetary_value_gbp,
    NTILE(5) OVER (ORDER BY c.last_invoice_date) AS recency_quintile,
    NTILE(5) OVER (ORDER BY c.frequency) AS frequency_quintile,
    NTILE(5) OVER (ORDER BY c.monetary_value) AS monetary_quintile
FROM customer_sales c
CROSS JOIN snapshot s
ORDER BY monetary_value_gbp DESC;
