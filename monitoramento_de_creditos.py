import pandas as pd
import streamlit as st
from functions.show_products import show_data_product_1
from functions.show_products import procces_filter

from st_pages import Page, show_pages, hide_pages

st.image('https://triggo.ai/assets/LOGO.svg', width=200)

show_pages([
    Page("visao_geral.py","Visão Geral"),
    Page("catalogo.py","Dataproduct Mercantil"),
    Page("reg_prod_2.py", "Dataproduct Mercantil - opção 2"),
    Page("monitoramento_de_creditos.py", " "),
    Page("monitoramento_de_creditos_2.py", "  ")
])

hide_pages([' '])
query = st.session_state.query
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
    'TAG_NAME': 'ANÁLISE_CRÉDITO',
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
    'TAG_NAME': 'ANÁLISE_AR',
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

df2['CREDITS_USED_PER_USER_APROX'] = df2['CREDITS_USED_PER_USER_APROX'].astype(float)
df2['TAG_NAME'] = df2['TAG_NAME'].str.replace('_', ' ')

list_of_products = df2['TAG_NAME'].unique()

#product = st.selectbox('Selecione o produto: ', list_of_products, help='Selecione o produto para visualizar os detalhes.', index=None,)
#st.write(st.session_state.btn_tag)
product = st.session_state.btn_tag
if product != None:
    df2 = df2[df2['TAG_NAME'] == product]
    show_data_product_1(df2, product)
