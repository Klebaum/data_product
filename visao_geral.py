import streamlit as st
import pandas as pd
import datetime
from datetime import date
from general_functions.show_func import score_card_geral, ranking_plot, pie_plot
from functions.credit_func import credit_billed_day, credit_billed_month, credit_billed_year, credit_sum_d, credit_sum_m, credit_sum_y
from functions.credit_func import plot_credit_billed_day, plot_credit_billed_month, plot_credit_billed_year
from functions.show_products import procces_filter
from st_pages import Page, show_pages, hide_pages

st.image('https://triggo.ai/assets/LOGO.svg', width=200)

query = pd.read_csv('Custo detalhado.csv')
df2 = pd.DataFrame(query)

show_pages([
    Page("catalogo.py","Registro de Produtos"),
    Page("visao_geral.py","Visão Geral"),
    Page("monitoramento_de_creditos.py"," ")
])

hide_pages([' '])

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

today = date.today()

df_aux = df2.copy()

df_aux['END_TIME'] = pd.to_datetime(df2['END_TIME'])
container1 = st.container()
col1, col2 = container1.columns([0.8, 1], gap="large")

title = 'VISÃO GERAL DOS PRODUTOS' 
col1.markdown(f'<p style="color:#29b5e8; font-family:Source Sans Pro, sans serif; font-size: 28px;"><b>{title}</b></p>', unsafe_allow_html=True)
col2.markdown('<p style="color:#29b5e8; font-family:Source Sans Pro, sans serif; font-size: 28px;"><b>CRÉDITOS COBRADOS SNOWFLAKE:</b></p>', unsafe_allow_html=True)

with col1:
    col1.write('Descrição: Previsão de vendas da loja X para os itens de jaqueta e guarda-chuva, com base no histórico de vendas e dados climáticos.')
    
    min_date = df_aux['END_TIME'].min()
    max_date = df_aux['END_TIME'].max()
    monitoring_date = col1.date_input('Selecione a data de monitoramento:', datetime.date(2024, 2, 9), min_value=min_date, max_value=max_date, help='A partir da data selecionada, será mostrada o gasto diário, mensal e anual.')

sum_d = credit_sum_d(df2, monitoring_date)
sum_m = credit_sum_m(df2, monitoring_date)
sum_y = credit_sum_y(df2, monitoring_date)

_, _, daily_credits = credit_billed_day(sum_d, monitoring_date, 'TAG_NAME')
_, _, monthly_credits = credit_billed_month(sum_m, monitoring_date, 'TAG_NAME')
_, _, yearly_credits = credit_billed_year(sum_y, monitoring_date, 'TAG_NAME')

score_card_geral(query, col2, daily_credits, monthly_credits, yearly_credits)

container = st.container(border=True)
col1, col2 = container.columns([0.8, 1], gap="large")

with col1:
    plot_credit_billed_day(sum_d, monitoring_date, col1, 'TAG_NAME')
with col2:
    plot_credit_billed_month(sum_m, monitoring_date, col2, 'TAG_NAME')
with container:
    plot_credit_billed_year(sum_m, monitoring_date, container, 'TAG_NAME')

container2 = st.container(border=True)
col1, col2 = container2.columns([0.8, 1], gap="large")

with col1:
    mult_rank = col1.multiselect('Selecione o(s) produto(s):', df2['TAG_NAME'].unique(), df2['TAG_NAME'].unique(), help='Selecione o processo para filtrar as informações.')
    try:
        selected_products = procces_filter(df2, mult_rank, 'TAG_NAME')
        ranking_plot(selected_products, col1,  mult_rank)
    except ValueError:
        col1.error('Selecione um produto para visualizar o ranking.')
with col2:
    mult_pie = col2.multiselect('Selecione o(s) produto(s):', df2['TAG_NAME'].unique(), df2['TAG_NAME'].unique(), help='Selecione o processo para filtrar as informações.', key=1)
    try:
        selected_products = procces_filter(df2, mult_pie, 'TAG_NAME')
        pie_plot(selected_products, col1,  mult_rank)
    except ValueError:
        col2.error('Selecione um produto para visualizar a porcentagem de consumo de cada produto.')
