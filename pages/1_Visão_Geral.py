import streamlit as st
import pandas as pd
import datetime
from datetime import date
from general_functions.credit_general  import show_data_general
from general_functions.show_func import score_card_geral
from functions.credit_func import credit_billed_day, credit_billed_month, credit_billed_year, credit_sum_d, credit_sum_m
from functions.credit_func import plot_credit_billed_day, plot_credit_billed_month, plot_credit_billed_year

query = pd.read_csv('Custo detalhado.csv')
df2 = pd.DataFrame(query)
today = date.today()

df_aux = df2.copy()
df_aux['END_TIME'] = pd.to_datetime(df2['END_TIME'])
container1 = st.container()
col1, col2 = container1.columns([0.8, 1], gap="large")

title = 'VISÃO GERAL DOS PRODUTOS' 
col1.title(f'{title}: ')
col2.title('CRÉDITOS COBRADOS SNOWFLAKE:')

with col1:
    col1.write('Descrição: Previsão de vendas da loja X para os itens de jaqueta e guarda-chuva, com base no histórico de vendas e dados climáticos.')
    
    min_date = df_aux['END_TIME'].min()
    max_date = df_aux['END_TIME'].max()
    monitoring_date = col1.date_input('Selecione a data de monitoramento:', datetime.date(2024, 2, 9), min_value=min_date, max_value=max_date, help='A partir da data selecionada, será mostrada o gasto diário, mensal e anual.')

sum_d = credit_sum_d(df2, monitoring_date)
sum_m = credit_sum_m(df2, monitoring_date)

_, _, daily_credits = credit_billed_day(sum_d, monitoring_date, 'TAG_NAME')
_, _, monthly_credits = credit_billed_month(sum_m, monitoring_date, 'TAG_NAME')
_, _, yearly_credits = credit_billed_year(sum_m, monitoring_date, 'TAG_NAME')

score_card_geral(query, col2, yearly_credits, monthly_credits, daily_credits)

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
    mult_rank = col1.multiselect('Selecione o(s) processo(s):', query['QUERY_TAG'].unique(), query['QUERY_TAG'].unique(), help='Selecione o processo para filtrar as informações.')
with col2:
    mult_porcentage = col2.multiselect('Selecione o(s) processo(s):', query['QUERY_TAG'].unique(), query['QUERY_TAG'].unique(), key=1, help='Selecione o processo para filtrar as informações.')

