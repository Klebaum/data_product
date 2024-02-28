import pandas as pd
import streamlit as st
import datetime
from datetime import date
import plotly.express as px
# from snowflake.snowpark.context import get_active_session
from functions.show_products import show_all_products
from functions.credit_func import credit_billed_day, credit_billed_month, credit_billed_year, credit_sum_d, credit_sum_m
st.set_page_config(layout="wide")

# query = "select owner, tag_name, obj_name, tag_value, end_time, source, query_tag, refresh_value, credits_used_per_user_aprox from streamlit_hierarchy_viewer.ml_forecasting.FORECAST_PRODUCT_v2 order by query_tag;"
query = pd.read_csv('Custo detalhado.csv')

df2 = pd.DataFrame(query)
df2['CREDITS_USED_PER_USER_APROX'] = df2['CREDITS_USED_PER_USER_APROX'].astype(float)

today = date.today()

sum_d = credit_sum_d(df2, today)
sum_m = credit_sum_m(df2, today)

_, _, daily_credits = credit_billed_day(sum_d, today)
_, _, monthly_credits = credit_billed_month(sum_m, today)
_, _, yearly_credits = credit_billed_year(sum_m, today)

show_all_products(query, today, daily_credits, monthly_credits, yearly_credits)
