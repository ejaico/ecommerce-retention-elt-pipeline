# 🛍️ E-Commerce Customer Retention & Funnel ELT Pipeline

An automated, production-grade ELT data pipeline built with **Python**, **DuckDB**, **dbt Core**, and **GitHub Actions** to process e-commerce REST API payloads, construct RFM customer segmentation models, compute 30-day cohort retention rates, and analyze behavioral conversion funnels.

---

## 🏗️ Pipeline Architecture & Tech Stack

```text
[ REST API / Synthetic Event Streams ] 
          │
          ▼  (Python Ingestion & DuckDB Raw Load)
[ DuckDB Raw Layer ] (raw.users, raw.orders, raw.events)
          │
          ▼  (dbt Core Modular Staging Transformations)
[ dbt Staging Layer ] (stg_customers, stg_orders, stg_events)
          │
          ▼  (Kimball Star Schema & RFM Logic)
[ dbt Marts Layer ] (dim_customers, fact_orders)
          │
          ▼  (Cohort & Funnel Analytics Models)
[ dbt Analytics Layer ] (analytics_cohort_retention, analytics_conversion_funnel)
          │
          ▼  (Automated Testing & BI Dashboards)
[ GitHub Actions Nightly Run ] ──> [ Streamlit / Power BI Dashboard ]
```

* **Ingestion & Storage:** Python (`requests`, `pandas`), DuckDB
* **Transformation & Modeling:** dbt Core (`dbt-duckdb`), SQL (CTEs, Window Functions, Aggregate Logic)
* **Data Quality & Governance:** dbt Schema Tests (`unique`, `not_null`, referential integrity)
* **Orchestration:** GitHub Actions CI/CD workflow (scheduled nightly at midnight)
* **Visualization:** Power BI

---

## 📊 dbt Data Lineage Graph (DAG)

* (Drag and drop your dbt Lineage Graph screenshot image here)*

---

## 💡 Key Business Metrics & Analytics Delivered

1. **RFM Customer Segmentation:**
   * Classified customer base into behavioral cohorts (`Champions / VIP`, `Loyal Customers`, `New Customers`, `At Risk / Churned`).
2. **Promotion & Incentive ROI:**
   * Analyzed margin impact of promotional discount codes (`SUMMER20`, `PROMO10`, `WELCOME15`) on net order revenue.
3. **Behavioral Conversion Funnel:**
   * Measured step-by-step user drop-offs across session events (page_view $\rightarrow$ product_view $\rightarrow$ add_to_cart $\rightarrow$ checkout_start $\rightarrow$ purchase).

---

## 🛠️ How to Run This Project Locally

**Clone the repository:**
   ```bash
   git clone https://github.com/ejaico/ecommerce-retention-elt-pipeline.git
   cd healthtech-quality-measures-pipeline