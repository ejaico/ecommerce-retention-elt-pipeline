WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),
orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
max_date_cte AS (
    SELECT MAX(order_date) AS max_dataset_date FROM orders
),
customer_stats AS (
    SELECT
        o.customer_id,
        MIN(o.order_date) AS first_order_date,
        MAX(o.order_date) AS most_recent_order_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(o.net_amount) AS total_lifetime_spend,
        AVG(o.net_amount) AS avg_order_value,
        DATE_DIFF('day', MAX(o.order_date), (SELECT max_dataset_date FROM max_date_cte)) AS recency_days
    FROM orders o
    GROUP BY o.customer_id
)
SELECT
    c.customer_id,
    c.email,
    c.first_name,
    c.last_name,
    c.city,
    cs.first_order_date,
    cs.most_recent_order_date,
    COALESCE(cs.total_orders, 0) AS total_orders,
    COALESCE(cs.total_lifetime_spend, 0.0) AS total_lifetime_spend,
    COALESCE(cs.avg_order_value, 0.0) AS avg_order_value,
    COALESCE(cs.recency_days, 999) AS recency_days,
    -- RFM Segmentation Logic
    CASE 
        WHEN cs.total_orders >= 4 AND cs.recency_days <= 15 THEN 'Champions / VIP'
        WHEN cs.total_orders BETWEEN 2 AND 3 AND cs.recency_days <= 30 THEN 'Loyal Customers'
        WHEN cs.total_orders = 1 AND cs.recency_days <= 30 THEN 'New Customers'
        WHEN cs.recency_days > 45 THEN 'At Risk / Churned'
        ELSE 'Regular'
    END AS rfm_segment
FROM customers c
LEFT JOIN customer_stats cs ON c.customer_id = cs.customer_id