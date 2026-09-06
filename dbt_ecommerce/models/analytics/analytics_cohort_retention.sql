WITH customer_first_order AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM {{ ref('stg_orders') }}
    GROUP BY customer_id
),
customer_activities AS (
    SELECT DISTINCT
        o.customer_id,
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) AS activity_month,
        DATE_DIFF('month', c.cohort_month, DATE_TRUNC('month', o.order_date)) AS month_number
    FROM {{ ref('stg_orders') }} o
    JOIN customer_first_order c ON o.customer_id = c.customer_id
)
SELECT
    cohort_month,
    month_number,
    COUNT(DISTINCT customer_id) AS active_retained_customers
FROM customer_activities
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number