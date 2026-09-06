WITH event_counts AS (
    SELECT
        event_type,
        COUNT(DISTINCT event_id) AS total_events,
        COUNT(DISTINCT customer_id) AS unique_users
    FROM {{ ref('stg_events') }}
    GROUP BY event_type
)
SELECT
    event_type,
    total_events,
    unique_users,
    CASE 
        WHEN event_type = 'page_view' THEN 1
        WHEN event_type = 'product_view' THEN 2
        WHEN event_type = 'add_to_cart' THEN 3
        WHEN event_type = 'checkout_start' THEN 4
        WHEN event_type = 'purchase' THEN 5
    END AS funnel_step
FROM event_counts
ORDER BY funnel_step