import pandas as pd
import streamlit as st
from functions.show_products import show_data_product_2, credit_billed_day, credit_billed_month, credit_billed_year, credit_sum_d, credit_sum_m, credit_sum_y
from functions.show_products import procces_filter
query = pd.read_csv('Custo detalhado.csv')
from st_pages import Page, show_pages, hide_pages
from datetime import date

st.image('https://triggo.ai/assets/LOGO.svg', width=200)

show_pages([
    Page("catalogo.py","Registro de Produtos"),
    Page("visao_geral.py","Visão Geral"),
    Page("reg_prod_2.py", "Registro de Produtos 2"),
    Page("monitoramento_de_creditos.py", " "),
    Page("monitoramento_de_creditos_2.py", "  ")
])

hide_pages([' '])

dtypes = pd.DataFrame(query).astype({'CREDITS_USED_PER_USER_APROX':'float'}).dtypes.values

df2 = pd.DataFrame(query)

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

# Criando um DataFrame a partir da nova entrada
new_row_df = pd.DataFrame([new_entry])
new_row_df2 = pd.DataFrame([new_entry2])
new_row_df3 = pd.DataFrame([new_entry3])
new_row_df4 = pd.DataFrame([new_entry4])

# Concatenando o novo DataFrame com o DataFrame existente
df2 = pd.concat([df2, new_row_df, new_row_df2, new_row_df3, new_row_df4], ignore_index=True)

today = date.today()

df2['CREDITS_USED_PER_USER_APROX'] = df2['CREDITS_USED_PER_USER_APROX'].astype(float)
df2['TAG_NAME'] = df2['TAG_NAME'].str.replace('_', ' ')
list_of_products = df2['TAG_NAME'].unique()

product = st.session_state.btn_tag_2

if product != None:
    df_aux = df2[df2['TAG_NAME'] == product]

    sum_d = credit_sum_d(df_aux, today)
    sum_m = credit_sum_m(df_aux, today)
    sum_y = credit_sum_y(df_aux, today)
    
    _, _, daily_credits = credit_billed_day(sum_d, today)
    _, _, monthly_credits = credit_billed_month(sum_m, today)
    _, _, yearly_credits = credit_billed_year(sum_y, today)
    description = "Descrição do produto"

    show_data_product_2(df_aux, product, today, daily_credits, monthly_credits, yearly_credits, description)
