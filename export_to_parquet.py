import duckdb

con = duckdb.connect('ecommerce.duckdb')

tables = [
    'dim_customers',
    'fact_orders',
    'analytics_cohort_retention',
    'analytics_conversion_funnel'
]

for table in tables:
    con.execute(f"COPY (SELECT * FROM main.{table}) TO '{table}.parquet' (FORMAT PARQUET);")
    print(f"Exported {table}.parquet successfully!")

con.close()