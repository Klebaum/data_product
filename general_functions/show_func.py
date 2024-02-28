import pandas as pd
import streamlit as st
import datetime

def score_card_geral(query, col2, daily_credits, monthly_credits, yearly_credits):
    df = pd.DataFrame(query)

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

def ranking_plot():
    pass