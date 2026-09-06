WITH source AS (
    SELECT * FROM raw.users
)
SELECT
    id AS customer_id
    , email
    , username
    , name.firstname AS first_name
    , name.lastname AS last_name
    , address.city AS city
    , address.zipcode AS zip_code
    , phone
FROM source