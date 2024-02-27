import pandas as pd
import streamlit as st
import datetime

import pandas as pd
from functions.credit_func import credit_sum_m, credit_sum_d, plot_credit_billed_day, plot_credit_billed_month, plot_credit_billed_year
from functions.credit_func import credit_billed_year, credit_billed_month, credit_billed_day
from functions.graph_func import make_graph

def procces_filter(query, filters):
    dfs = [] 

    for filter in filters:
        filtered_df = query[query['QUERY_TAG'] == filter] 
        dfs.append(filtered_df)  
    concatenated_df = pd.concat(dfs, ignore_index=True) 
    return concatenated_df

def show_all_products(query):
    container1 = st.container(border=True)
    col1, col2 = container1.columns(2)
    
    n_tables = len(query['OBJ_NAME'].unique())

    # Preencher pelos dados da tabela
    with col1:
        title = query['TAG_NAME'].astype(str).unique()[0].replace('_', ' ')
        col1.title(f'{title}: ')
        col1.write(f'Owner: {query["OWNER"].unique()[0]}')
        col1.write(f'Quantidade de objetos: {n_tables}')
        col1.write('Descrição: Previsão de vendas da loja X para os itens de jaqueta e guarda-chuva, com base no histórico de vendas e dados climáticos.')
        with col1.expander('Detalhes das informações do produto'):
            aux = (f'As informações foram retiradas a partir de um trabalho de "Tagging" dos objetos e processos'+
                   f' realizados no Snowflake para o {title}. Os objetos são atualizados a cada hora.')
            st.write(aux)

    with col2:
        col2.title("Data Product 2: ")
        col2.write('Owner: -')
        col2.write('Quantidade de tabelas: -')
        col2.write('Descrição: -')
    container1.divider()


def score_cards(daily_credits, monthly_credits, yearly_credits):
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
                
    title_col, btc_col, eth_col, xmr_col, sol_col, xrp_col = st.columns([0.8,0.3,0.3,0.3,1,1])

    with title_col:
        st.markdown('<p class="dashboard_title">Créditos Cobrados<br>Snowflake</p>', unsafe_allow_html = True)

    with btc_col:
        with st.container(border=True):
            st.markdown(f'<p class="btc_text">ANUAL<br></p><p class="price_details">{yearly_credits}</p>', unsafe_allow_html = True)

    with eth_col:
        with st.container(border=True):
            st.markdown(f'<p class="eth_text">MONTHLY<br></p><p class="price_details">{monthly_credits}</p>', unsafe_allow_html = True)

    with xmr_col:
        with st.container(border=True):
            st.markdown(f'<p class="xmr_text">DAILY<br></p><p class="price_details">{daily_credits}</p>', unsafe_allow_html = True)


def show_data_product_1(query):
    st.session_state["query"] = query
    dtypes = pd.DataFrame(query).astype({'CREDITS_USED_PER_USER_APROX':'float'}).dtypes.values
    #   return rows, cols, colsN

    # rows, cols, colsN = runQuery(query)
    #st.write(rows)
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
    
    # Criando um DataFrame a partir da nova entrada
    new_row_df = pd.DataFrame([new_entry])
    new_row_df2 = pd.DataFrame([new_entry2])
    
    # Concatenando o novo DataFrame com o DataFrame existente
    df2 = pd.concat([df2, new_row_df, new_row_df2], ignore_index=True)

    df2['CREDITS_USED_PER_USER_APROX'] = df2['CREDITS_USED_PER_USER_APROX'].astype(float)

    #df = st.dataframe(df2, use_container_width=True)
    row = st.columns(2)

    container0 = st.container()
    col1, col2 = container0.columns(2)

    title = query['TAG_NAME'].astype(str).unique()[0].replace('_', ' ')
    col1.title(f'{title}:')
    col1.header('Monitoramento de Créditos Cobrados')
    col1.subheader('Data de monitoramento e processos: ')

    # Definindo min e max para o date_input
    df_aux = df2.copy()
    df_aux['END_TIME'] = pd.to_datetime(df_aux['END_TIME'])
    
    min_date = df_aux['END_TIME'].min()
    max_date = df_aux['END_TIME'].max()

    container1 = st.container()
    col1, col2 = container1.columns(2)
    container1_2 = st.container()
    col1_2, col2_2 = container1_2.columns(2)
    col1.text('Processos que fazem parte do Data Product.')

    procces = col1_2.multiselect('Selecione o(s) processo(s):', df2['QUERY_TAG'].unique(), df2['QUERY_TAG'].unique(), help='Selecione o processo para filtrar as informações.')
    col2.text('A data de monitoramento ao ser definida, mostrará o gasto diário e do mês da data \nselecionada.')
    monitoring_date = col2_2.date_input('Selecione a data de monitoramento:', datetime.date(2024, 2, 9), min_value=min_date, max_value=max_date, help='A partir da data selecionada, será mostrada o gasto diário e total do mês.')



    if len(procces) != 0:
        df_selected_procces = procces_filter(df2, procces)
        sum_d = credit_sum_d(df_selected_procces, monitoring_date) 
        sum_m = credit_sum_m(df_selected_procces, monitoring_date)

        _, _, daily_credits = credit_billed_day(sum_d, monitoring_date)
        _, _, monthly_credits = credit_billed_month(sum_m, monitoring_date)
        _, _, yearly_credits = credit_billed_year(sum_m, monitoring_date)

        score_cards(daily_credits, monthly_credits, yearly_credits)

        
        container2 = st.container(border=True)            
        col1, col2 = container2.columns(2)

        with col1:
            plot_credit_billed_day(sum_d, monitoring_date, col1)
        with col2:
            plot_credit_billed_month(sum_m, monitoring_date, col2)
        with container2:
            plot_credit_billed_year(sum_m, monitoring_date, container2)
    container3 = st.container(border=True)
    container3.subheader('Grafo de Processos mensal:')
    dot = make_graph(df2)    
    container3.graphviz_chart(dot)


    date_to_filter = pd.to_datetime(monitoring_date).strftime('%Y-%m-%d')
    df_daily_graph = df2[df2['END_TIME'] == date_to_filter]
    # st.write(df2)
    container3.subheader('Grafo de Processos diário:')
    dot = make_graph(df_daily_graph)
    container3.graphviz_chart(dot)

def show_home_content_dp2():
    st.write("Conteúdo da aba Home")

def show_tables_graphs_content_dp2():
   st.write("Produto indisponível")

def show_graph_content_dp2():
    st.write("Produto indisponível")
    
def show_data_product_2():
    sub_tab = st.radio("Selecione uma sub aba:", ("Home", "Tabelas/Gráficos", "Grafo"))
    if sub_tab == "Home":
        show_home_content_dp2()
    elif sub_tab == "Tabelas/Gráficos":
        show_tables_graphs_content_dp2()