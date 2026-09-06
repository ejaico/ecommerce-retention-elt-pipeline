WITH source AS (
    SELECT * FROM raw.events
)
SELECT
    event_id
    , user_id AS customer_id
    , event_type
    , CAST(event_timestamp AS TIMESTAMP) AS event_timestamp
    , CAST(event_timestamp AS DATE) AS event_date
FROM source