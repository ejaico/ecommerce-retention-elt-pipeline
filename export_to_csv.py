import duckdb

con = duckdb.connect('ecommerce.duckdb')
con.execute("COPY (SELECT * FROM main.dim_customers) TO 'dim_customers.csv' (HEADER, DELIMITER ',');")
con.execute("COPY (SELECT * FROM main.fact_orders) TO 'fact_orders.csv' (HEADER, DELIMITER ',');")
con.execute("COPY (SELECT * FROM main.analytics_cohort_retention) TO 'analytics_cohort_retention.csv' (HEADER, DELIMITER ',');")
con.execute("COPY (SELECT * FROM main.analytics_conversion_funnel) TO 'analytics_conversion_funnel.csv' (HEADER, DELIMITER ',');")
print("CSV exports complete!")
con.close()