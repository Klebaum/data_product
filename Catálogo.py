import pandas as pd
import streamlit as st
import datetime
import plotly.express as px
# from snowflake.snowpark.context import get_active_session
from functions.show_products import show_all_products, show_data_product_1, show_data_product_2

st.set_page_config(layout="wide")

# query = "select owner, tag_name, obj_name, tag_value, end_time, source, query_tag, refresh_value, credits_used_per_user_aprox from streamlit_hierarchy_viewer.ml_forecasting.FORECAST_PRODUCT_v2 order by query_tag;"
query = pd.read_csv('Custo detalhado.csv')

show_all_products(query)
