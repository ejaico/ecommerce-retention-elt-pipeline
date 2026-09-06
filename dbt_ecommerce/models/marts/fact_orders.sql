WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
)
SELECT
    o.order_id,
    o.customer_id,
    o.order_timestamp,
    o.order_date,
    o.product_id,
    o.category,
    o.quantity,
    o.unit_price,
    o.gross_amount,
    o.discount_code,
    o.discount_amount,
    o.net_amount,
    -- Margin Metrics & Promotion Flag
    ROUND(o.net_amount * 0.40, 2) AS estimated_gross_margin,
    CASE WHEN o.discount_amount > 0 THEN TRUE ELSE FALSE END AS is_discounted_order
FROM orders o