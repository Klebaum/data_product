import streamlit as st
import pandas as pd
import datetime
from datetime import date
from general_functions.credit_general  import show_data_general
from general_functions.show_func import score_card_geral
from functions.credit_func import credit_billed_day, credit_billed_month, credit_billed_year, credit_sum_d, credit_sum_m

query = pd.read_csv('Custo detalhado.csv')
today = date.today()

moniring_date = score_card_geral(query, 50, 20, 30)

container = st.container(border=True)
col1, col2 = container.columns(2)

with col1:
    col1.subheader('Diários')
with col2:
    col2.subheader('Mensais')
container.subheader('Anuais')



