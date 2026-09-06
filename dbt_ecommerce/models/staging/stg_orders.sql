WITH source AS (
    SELECT * FROM raw.orders
)
SELECT
    order_id
    , user_id AS customer_id
    , CAST(order_timestamp AS TIMESTAMP) AS order_timestamp
    , CAST(order_timestamp AS DATE) AS order_date
    , product_id
    , category
    , quantity
    , unit_price
    , gross_amount
    , discount_code
    , discount_amount
    , net_amount
FROM source