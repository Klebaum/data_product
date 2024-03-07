import pandas as pd
import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
import datetime
from datetime import date
import plotly.express as px
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
from functions.show_products import show_all
from functions.credit_func import credit_billed_day, credit_billed_month, credit_billed_year, credit_sum_d, credit_sum_m, credit_sum_y
from st_pages import Page, show_pages, hide_pages

from sessions_func.create_session import runQuery
from st_keyup import st_keyup

query = "select owner, tag_name, obj_name, tag_value, end_time, source, query_tag, refresh_value, credits_used_per_user_aprox from streamlit_hierarchy_viewer.ml_forecasting.FORECAST_PRODUCT_v2 order by query_tag;"
data = runQuery(query)

st.image('https://triggo.ai/assets/LOGO.svg', width=200)

# key to btn
st.session_state.key_value_2 = 0 
#st.session_state.btn_tag_2 = ''
#query = pd.read_csv('Custo detalhado.csv')

df2 = pd.DataFrame(data)
st.session_state.query = df2

# Dados sintéticos
new_entry = {
        'OWNER': 'MERCANTIL',
        'WAREHOUSE_NAME': 'COMPUTE_WH',
        'TAG_NAME': 'FORECAST_DATA_PRODUCT',
        'END_TIME': '2024-02-10',
        'SOURCE': 'forecast_ml',
        'QUERY_TAG': 'results',
        'DATABASE_NAME': 'STREAMLIT_HIERARCHY_VIEWER',
        'SCHEMA_NAME': 'ML_FORECASTING',
        'TABLE_VIEW_NAME': 'STREAMLIT_HIERARCHY_VIEWER.ML_FORECASTING.V4_FORECAST',
        'TAG_VALUE': 'view',
        'OBJ_NAME': 'V4_FORECAST',
        'REFRESH_VALUE': 'hourly',
        'CREDITS_USED_PER_USER_APROX': 0.058
    }

new_entry2 = {
    'OWNER': 'MERCANTIL',
    'WAREHOUSE_NAME': 'COMPUTE_WH',
    'TAG_NAME': 'FORECAST_DATA_PRODUCT',
    'END_TIME': '2024-02-10',
    'SOURCE': 'forecast_transform',
    'QUERY_TAG': 'forecast_ml',
    'DATABASE_NAME': 'STREAMLIT_HIERARCHY_VIEWER',
    'SCHEMA_NAME': 'ML_FORECASTING',
    'TABLE_VIEW_NAME': 'STREAMLIT_HIERARCHY_VIEWER.ML_FORECASTING.V4',
    'TAG_VALUE': 'view',
    'OBJ_NAME': 'V4',
    'REFRESH_VALUE': 'hourly',
    'CREDITS_USED_PER_USER_APROX': 0.58
}

new_entry3 = {
    'OWNER': 'MERCANTIL',
    'WAREHOUSE_NAME': 'COMPUTE_WH',
    'TAG_NAME': 'PRODUTO_A',
    'END_TIME': '2024-02-09',
    'SOURCE': 'procces_1',
    'QUERY_TAG': 'result',
    'DATABASE_NAME': 'STREAMLIT_HIERARCHY_VIEWER',
    'SCHEMA_NAME': 'ML_FORECASTING',
    'TABLE_VIEW_NAME': 'STREAMLIT_HIERARCHY_VIEWER.ML_FORECASTING.V4_FORECAST',
    'TAG_VALUE': 'view',
    'OBJ_NAME': 'V4_FORECAST',
    'REFRESH_VALUE': 'hourly',
    'CREDITS_USED_PER_USER_APROX': 1.58
}

new_entry4 = {
    'OWNER': 'MERCANTIL',
    'WAREHOUSE_NAME': 'COMPUTE_WH',
    'TAG_NAME': 'PRODUTO_B',
    'END_TIME': '2024-02-10',
    'SOURCE': 'procces_2',
    'QUERY_TAG': 'procces_1',
    'DATABASE_NAME': 'STREAMLIT_HIERARCHY_VIEWER',
    'SCHEMA_NAME': 'ML_FORECASTING',
    'TABLE_VIEW_NAME': 'STREAMLIT_HIERARCHY_VIEWER.ML_FORECASTING.V4',
    'TAG_VALUE': 'view',
    'OBJ_NAME': 'V4',
    'REFRESH_VALUE': 'hourly',
    'CREDITS_USED_PER_USER_APROX': 0.58
}


new_row_df = pd.DataFrame([new_entry])
new_row_df2 = pd.DataFrame([new_entry2])
new_row_df3 = pd.DataFrame([new_entry3])
new_row_df4 = pd.DataFrame([new_entry4])

df2 = pd.concat([df2, new_row_df, new_row_df2, new_row_df3, new_row_df4], ignore_index=True)


df2['CREDITS_USED_PER_USER_APROX'] = df2['CREDITS_USED_PER_USER_APROX'].astype(float)
df2['TAG_NAME'] = df2['TAG_NAME'].str.replace('_', ' ')
today = date.today()

list_products = df2['TAG_NAME'].unique()

filter = st_keyup("Pesquisar Produto")

# filtro que a partir do que é digitado no search, ele filtre os produtos que contém o que foi digitado
# e mostre apenas esses produtos
df_aux = df2[df2['TAG_NAME'].str.startswith(filter.upper(), len(filter))]
# st.write(df_aux['TAG_NAME'].unique())
list_products = df_aux['TAG_NAME'].unique()

show_all(df_aux, today, 1, 1, 1, 'asd')