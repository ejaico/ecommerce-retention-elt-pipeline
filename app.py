import streamlit as st
import duckdb
import plotly.express as px

st.set_page_config(page_title="E-Commerce Retention & Funnel Dashboard", layout="wide")
st.title("🛍️ E-Commerce Customer Retention & Funnel Analytics")

con = duckdb.connect("ecommerce.duckdb")

df_rfm = con.execute("SELECT rfm_segment, COUNT(*) as customer_count, SUM(total_lifetime_spend) as total_revenue FROM main.dim_customers GROUP BY rfm_segment").df()
df_funnel = con.execute("SELECT * FROM main.analytics_conversion_funnel ORDER BY funnel_step").df()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer RFM Segmentation Breakdown")
    fig_rfm = px.pie(df_rfm, names="rfm_segment", values="customer_count", title="Customer Distribution by Segment")
    st.plotly_chart(fig_rfm, use_container_width=True)

with col2:
    st.subheader("E-Commerce Behavioral Conversion Funnel")
    fig_funnel = px.funnel(df_funnel, x="unique_users", y="event_type", title="Conversion Funnel Step-by-Step")
    st.plotly_chart(fig_funnel, use_container_width=True)