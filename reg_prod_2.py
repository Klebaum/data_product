import pandas as pd
import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
import datetime
from datetime import date
import plotly.express as px
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
#from functions.show_products import show_all_products
from functions.credit_func import credit_billed_day, credit_billed_month, credit_billed_year, credit_sum_d, credit_sum_m, credit_sum_y
from st_pages import Page, show_pages, hide_pages
from streamlit_extras.grid import grid
from sessions_func.create_session import runQuery
from st_keyup import st_keyup

show_pages([
    Page("catalogo.py","Registro de Produtos"),
    Page("visao_geral.py","Visão Geral"),
    Page("monitoramento_de_creditos.py"," ")
])

hide_pages([' '])


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

    st.markdown(
    """
    <style>
        /* Classe de estilo para modificar o container */
        .custom-container {
            font-family: Source Sans Pro;
            font-size: 20px; 
            color: #29b5e8;
            font-weight: bold;
            text-align: center;
            line-height: 0.2;
            padding-top: 10px;
        }

        .custom-text {
            font-family: Source Sans Pro;
            font-size: 16px; 
            color: #3d3d3c;
            text-align: center;
            line-height: 0.2;
            padding-top: 10px;
        }
        
        .centered-image {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
    )

    my_grid = grid(3, 3, 3, vertical_align="top", gap="medium")
    containerh = my_grid.container(border=True)
    containerh.markdown("<p class='custom-container'>FORECAST DATA PRODUCT</p>", unsafe_allow_html=True)
    containerh.markdown("<p class='centered-image'><img src='https://triggo.ai/assets/LOGO.svg' width='150'></p>", unsafe_allow_html=True)
    containerh.markdown("<p class='custom-text'>A descrição do produto viria aqui onde<br/><br/><br/><br/>podemos colocar algo bem resumido</p>", unsafe_allow_html=True)
    containerh.columns([1, 1], gap="small")
    containerh.button('Análise de créditos', key=31, use_container_width=True)

    containerh = my_grid.container(border=True)
    containerh.markdown("<p class='custom-container'>PRODUTO A</p>", unsafe_allow_html=True)
    containerh.markdown("<p class='centered-image'><img src='https://triggo.ai/assets/LOGO.svg' width='150'></p>", unsafe_allow_html=True)
    containerh.markdown("<p class='custom-text'>A descrição do produto viria aqui onde<br/><br/><br/><br/>podemos colocar algo bem resumido</p>", unsafe_allow_html=True)
    containerh.columns([1, 1], gap="small")
    containerh.button('Análise de créditos', key=32, use_container_width=True)

    containerh = my_grid.container(border=True)
    containerh.markdown("<p class='custom-container'>PRODUTO B</p>", unsafe_allow_html=True)
    containerh.markdown("<p class='centered-image'><img src='https://triggo.ai/assets/LOGO.svg' width='150'></p>", unsafe_allow_html=True)
    containerh.markdown("<p class='custom-text'>A descrição do produto viria aqui onde<br/><br/><br/><br/>podemos colocar algo bem resumido</p>", unsafe_allow_html=True)
    containerh.columns([1, 1], gap="small")
    containerh.button('Análise de créditos', key=33, use_container_width=True)


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
            #switch_page(' ')

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




query = "select owner, tag_name, obj_name, tag_value, end_time, source, query_tag, refresh_value, credits_used_per_user_aprox from streamlit_hierarchy_viewer.ml_forecasting.FORECAST_PRODUCT_v2 order by query_tag;"
data = runQuery(query)

st.image('https://triggo.ai/assets/LOGO.svg', width=200)


# key to btn
st.session_state.key_value = 0 

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
# df2 = df2[df2['TAG_NAME'] == 'FORECAST_DATA_PRODUCT']
today = date.today()

list_products = df2['TAG_NAME'].unique()

filter = st_keyup("Pesquisar Produto")

# filtro que a partir do que é digitado no search, ele filtre os produtos que contém o que foi digitado
# e mostre apenas esses produtos
df_aux = df2[df2['TAG_NAME'].str.startswith(filter.upper(), len(filter))]
# st.write(df_aux['TAG_NAME'].unique())
list_products = df_aux['TAG_NAME'].unique()

for product in list_products:
    df_aux = df2[df2['TAG_NAME'] == product]

    sum_d = credit_sum_d(df_aux, today)
    sum_m = credit_sum_m(df_aux, today)
    sum_y = credit_sum_y(df_aux, today)
    
    _, _, daily_credits = credit_billed_day(sum_d, today)
    _, _, monthly_credits = credit_billed_month(sum_m, today)
    _, _, yearly_credits = credit_billed_year(sum_y, today)
    description = "Descrição do produto"

    show_all_products(df_aux, today, daily_credits, monthly_credits, yearly_credits, description)


