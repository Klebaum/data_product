import pandas as pd
import streamlit as st
import datetime

def score_card_geral(query, daily_credits, monthly_credits, yearly_credits):
    df = pd.DataFrame(query)

    df['END_TIME'] = pd.to_datetime(df['END_TIME'])
    container1 = st.container()
    col1, col2 = container1.columns([0.8, 1], gap="large")

    title = 'VISÃO GERAL DOS PRODUTOS' 
    col1.title(f'{title}: ')
    col2.title('CRÉDITOS COBRADOS SNOWFLAKE:')

    with col1:
        col1.write('Descrição: Previsão de vendas da loja X para os itens de jaqueta e guarda-chuva, com base no histórico de vendas e dados climáticos.')
        
        min_date = df['END_TIME'].min()
        max_date = df['END_TIME'].max()
        monitoring_date = col1.date_input('Selecione a data de monitoramento:', datetime.date(2024, 2, 9), min_value=min_date, max_value=max_date, help='A partir da data selecionada, será mostrada o gasto diário, mensal e anual.')

    with col2:
        st.markdown(
        """
        <style>
            footer {display: none}
            [data-testid="stHeader"] {display: none}
        </style>
        """, unsafe_allow_html = True
        )

        with open('assets/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)
                 
        btc_col, eth_col, xmr_col, x = st.columns([0.5,0.5,0.5,0.1], gap="medium")
        with btc_col:
            with st.container(border=True):
                st.markdown(f'<p class="btc_text">ANUAL<br></p><p class="price_details">{yearly_credits}</p>', unsafe_allow_html = True)

        with eth_col:
            with st.container(border=True):
                st.markdown(f'<p class="eth_text">MONTHLY<br></p><p class="price_details">{monthly_credits}</p>', unsafe_allow_html = True)

        with xmr_col:
            with st.container(border=True):
                st.markdown(f'<p class="xmr_text">DAILY<br></p><p class="price_details">{daily_credits}</p>', unsafe_allow_html = True)
    return monitoring_date

def general_daily_plot():
    pass

def general_monthly_plot():
    pass

def general_yearly_plot():
    pass