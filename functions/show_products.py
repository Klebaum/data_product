import pandas as pd
import streamlit as st
import datetime

import pandas as pd
from functions.credit_func import credit_sum_m, credit_sum_d, credit_sum_y, plot_credit_billed_day, plot_credit_billed_month, plot_credit_billed_year
from functions.credit_func import credit_billed_year, credit_billed_month, credit_billed_day
from functions.graph_func import make_graph
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages


def procces_filter(query, filters, var_to_filter='QUERY_TAG'):
    """_summary_

    Args:
        query (DataFrame): pandas DataFrame
        filters (list): filters to be applied to the query DataFrame.
        var_to_filter (str, optional): _description_. Defaults to 'QUERY_TAG'.

    Returns:
        DataFrame: dataframe with the filters applied.
    """
    
    dfs = [] 

    for filter in filters:
        filtered_df = query[query[var_to_filter] == filter] 
        dfs.append(filtered_df)  
    concatenated_df = pd.concat(dfs, ignore_index=True) 
    return concatenated_df

def show_all_products(query, today, daily_credits, monthly_credits, yearly_credits, description):
    """_summary_
    
    Args:
        query (DataFrame): pandas DataFrame
        today (datetime): date to be used in the analysis.
        daily_credits (float): daily credits to be used in the analysis.
        monthly_credits (float): monthly credits to be used in the analysis.
        yearly_credits (float): yearly credits to be used in the analysis.
        description (str): description of the data product.
    
    Returns:
        None: all products are shown in the page.
    """
    today = pd.to_datetime(today).strftime('%Y/%m/%d')
    
    container1 = st.container(border=True)
    col1, col2 = container1.columns([0.8, 1], gap="large")
    
    n_tables = len(query['OBJ_NAME'].unique())

    title = query['TAG_NAME'].astype(str).unique()[0].replace('_', ' ')
    col1.markdown(f'<p style="color:#29b5e8; font-family:Source Sans Pro, sans serif; font-size: 28px;"><b>{title}: </b></p> ', unsafe_allow_html=True)
    col2.markdown('<p style="color:#29b5e8; font-family:Source Sans Pro, sans serif; font-size: 28px;"><b>CRÉDITOS COBRADOS SNOWFLAKE:</b></p>', unsafe_allow_html=True)

    with col1:
        col1.write(f'Owner: {query["OWNER"].unique()[0]}')
        col1.write(f'Quantidade de objetos: {n_tables}')
        col1.write(f'Tempo de atualização: {query["REFRESH_VALUE"].unique()[0]}')
        query['END_TIME'] = pd.to_datetime(query['END_TIME'])
        max_date = query['END_TIME'].max()
        max_date = pd.to_datetime(max_date).strftime('%Y/%m/%d')
        col1.write(f'Última data de atualização: {max_date}')
        
        st.session_state.key_value += 1
        if st.button('Análise de créditos cobrados do produto', key=st.session_state.key_value):
            st.session_state.btn_tag = query['TAG_NAME'].unique()[0]
            switch_page(' ')

    with container1.expander('Descrição do produto'):
        aux = (f'As informações foram retiradas a partir de um trabalho de "Tagging" dos objetos e processos'+
                f' realizados no Snowflake para o {title}. Os objetos são atualizados a cada hora.')
        st.write(aux)
        st.write('Descrição: Previsão de vendas da loja X para os itens de jaqueta e guarda-chuva, com base no histórico de vendas e dados climáticos.')

        
    col2.write(f'Créditos cobrados na data atual {today}:')
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
                st.markdown(f'<p class="eth_text">MENSAL<br></p><p class="price_details">{monthly_credits}</p>', unsafe_allow_html = True)

        with xmr_col:
            with st.container(border=True):
                st.markdown(f'<p class="xmr_text">DIÁRIO<br></p><p class="price_details">{daily_credits}</p>', unsafe_allow_html = True)


def score_cards(daily_credits, monthly_credits, yearly_credits):
    """_summary_
    
    Args:
        daily_credits (float): daily credits to be used in the analysis.
        monthly_credits (float): monthly credits to be used in the analysis.
        yearly_credits (float): yearly credits to be used in the analysis.

    Returns:
        None: score cards are shown in the page.
    """
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
                
    x1, title_col, btc_col, eth_col, xmr_col, x = st.columns([0.1, 0.8,0.5,0.5,0.5,0.1], gap="large")

    with title_col:
        st.markdown('<p class="dashboard_title">Créditos Cobrados<br>Snowflake</p>', unsafe_allow_html = True)

    with btc_col:
        with st.container(border=True):
            st.markdown(f'<p class="btc_text">ANUAL<br></p><p class="price_details">{yearly_credits}</p>', unsafe_allow_html = True)

    with eth_col:
        with st.container(border=True):
            st.markdown(f'<p class="eth_text">MENSAL<br></p><p class="price_details">{monthly_credits}</p>', unsafe_allow_html = True)

    with xmr_col:
        with st.container(border=True):
            st.markdown(f'<p class="xmr_text">DIÁRIO<br></p><p class="price_details">{daily_credits}</p>', unsafe_allow_html = True)


def show_data_product_1(df2, product):
    """_summary_

    Args:
        df2 (DataFrame): pandas DataFrame
        product (str): product to be shown in the page.

    Returns:
        None: data product is shown in the page with Snowflake credit monitor.
    """
    container0 = st.container()
    col1, col2 = container0.columns(2)

    title = df2['TAG_NAME'].astype(str).unique()[0].replace('_', ' ')
    col1.markdown(f'<p style="color:#29b5e8; font-family:Source Sans Pro, sans serif; font-size: 30px;"><b>{title}:</b></p>', unsafe_allow_html=True)


    # Definindo min e max para o date_input
    df_aux = df2.copy()
    df_aux['END_TIME'] = pd.to_datetime(df_aux['END_TIME'])
    
    min_date = df_aux['END_TIME'].min()
    max_date = df_aux['END_TIME'].max() + pd.Timedelta(days=1)

    container1 = st.container()
    col1, col2 = container1.columns(2, gap="large")
    container1_2 = st.container()
    col1_2, col2_2 = container1_2.columns(2, gap="large")
    
    col1.markdown('<p style="color:#3d3d3c; font-family:Source Sans Pro, sans serif; font-size: 25px;"><b>Monitoramento de Créditos Cobrados</b></p>', unsafe_allow_html=True)

    procces = col1_2.multiselect('Selecione o(s) processo(s)que fazem parte do Data Product:', df2['QUERY_TAG'].unique(), df2['QUERY_TAG'].unique(), help='Selecione o processo para filtrar as informações.')
    col2.markdown('<p style="color:#3d3d3c; font-family:Source Sans Pro, sans serif; font-size: 25px;"><b>Data de monitoramento e processos: </b></p>', unsafe_allow_html=True)
    col2.write('A data de monitoramento ao ser definida, mostrará o gasto diário e do mês da data selecionada.')
    monitoring_date = col2_2.date_input('Selecione a data de monitoramento:', value=min_date, min_value=min_date, max_value=max_date, help='A partir da data selecionada, será mostrada o gasto diário e total do mês.')

    if len(procces) != 0:
        df_selected_procces = procces_filter(df2, procces)
        sum_d = credit_sum_d(df_selected_procces, monitoring_date) 
        sum_m = credit_sum_m(df_selected_procces, monitoring_date)
        sum_y = credit_sum_y(df_selected_procces, monitoring_date)

        _, _, daily_credits = credit_billed_day(sum_d, monitoring_date)
        _, _, monthly_credits = credit_billed_month(sum_m, monitoring_date)
        _, _, yearly_credits = credit_billed_year(sum_y, monitoring_date)

        score_cards(daily_credits, monthly_credits, yearly_credits)

        
        container2 = st.container(border=True)            
        col1, col2 = container2.columns(2, gap="medium")

        with col1:
            plot_credit_billed_day(sum_d, monitoring_date, col1)
        with col2:
            plot_credit_billed_month(sum_m, monitoring_date, col2)
        with container2:
            plot_credit_billed_year(sum_m, monitoring_date, container2)
    container3 = st.container(border=True)
    container3.markdown('<p style="color:#3d3d3c; font-family:Source Sans Pro, sans serif; font-size: 20px;"><b>Fluxograma de Processos mensal</b></p>', unsafe_allow_html=True)
    dot = make_graph(df2)    
    container3.graphviz_chart(dot)

    date_to_filter = pd.to_datetime(monitoring_date).strftime('%Y-%m-%d')
    df_daily_graph = df2[df2['END_TIME'] == date_to_filter]
    # st.write(df2)
    container3.markdown('<p style="color:#3d3d3c; font-family:Source Sans Pro, sans serif; font-size: 20px;"><b>Fluxograma de Processos diário</b></p>', unsafe_allow_html=True)
    dot = make_graph(df_daily_graph)
    container3.graphviz_chart(dot)
