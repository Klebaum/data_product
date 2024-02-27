import configparser, os
import pandas as pd
import streamlit as st
import datetime
import random
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session

# calculate the sum value of same tag_query
# Divide em dois para facilitar a lógica e ajustar bugs
def credit_sum_m(df, date_m):
    df['END_TIME'] = df['END_TIME'].dt.to_period('D').astype(str)
    monthly_sum = df.groupby(['END_TIME', 'QUERY_TAG', 'TAG_NAME'])['CREDITS_USED_PER_USER_APROX'].sum().reset_index()
    date_m_month_year = pd.to_datetime(date_m).strftime('%Y-%m')
    monthly_sum['END_TIME'] = monthly_sum['END_TIME'].astype(str)
    monthly_sum_filtered = monthly_sum[monthly_sum['END_TIME'].str.startswith(date_m_month_year)]
    return monthly_sum_filtered


def credit_sum_d(df, date_m):
    df['END_TIME'] = pd.to_datetime(df['END_TIME'])
    daily_sum = df.groupby([df['END_TIME'].dt.date, 'QUERY_TAG', 'TAG_NAME'])['CREDITS_USED_PER_USER_APROX'].sum().reset_index()

    return daily_sum

# Plot dos gráficos usando o st.bar_chart
def plot_credit_billed_month(df, date):
    adjust_d = df.pivot_table(index='END_TIME', columns='QUERY_TAG', values='CREDITS_USED_PER_USER_APROX', aggfunc='sum')
    adjust_d.reset_index(inplace=True)

    # Convert 'END_TIME' to date format
    adjust_d['END_TIME'] = pd.to_datetime(adjust_d['END_TIME']).dt.date
    
    date_to_filter = pd.to_datetime(date).strftime('%Y/%m')
    
    adjust_d['Total'] = adjust_d[df['QUERY_TAG'].unique()].sum(axis=1)
    total_credits = adjust_d['Total'].sum()

    # Plotting with Plotly
    fig = px.bar(adjust_d, x='END_TIME', y=df['QUERY_TAG'],
                 title=f'Créditos gastos no mês {date_to_filter}')


    # Add total value annotation
    fig.add_annotation(x=adjust_d['END_TIME'].iloc[-1], y=total_credits,
                       text=f'Total: {round(total_credits, 2)}',
                       showarrow=False,
                       font=dict(color='black', size=16),
                       xanchor='center', yanchor='bottom')

    fig.update_layout(xaxis_title='DATA', yaxis_title='CRÉDITOS COBRADOS', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

# Plot dos gráficos usando o st.bar_chart
def plot_credit_billed_day(df, date):
    if df['END_TIME'].dtype != 'object':
        df['END_TIME'] = df['END_TIME'].astype(str)

    df['END_TIME'] = pd.to_datetime(df['END_TIME'], format='%Y/%m/%d')

    date_to_filter = pd.to_datetime(date).strftime('%Y/%m/%d')
    df_filtered = df[df['END_TIME'].dt.strftime('%Y/%m/%d') == date_to_filter]

    adjust_d = df_filtered.pivot_table(index='QUERY_TAG', values='CREDITS_USED_PER_USER_APROX',  aggfunc='sum')
    adjust_d.reset_index(inplace=True)

    total_credits = adjust_d['CREDITS_USED_PER_USER_APROX'].sum()  # Assuming single row for the filtered date

    fig = px.bar(adjust_d, x='QUERY_TAG', y='CREDITS_USED_PER_USER_APROX', title=f'Créditos gastos no dia {date_to_filter}')
    
    # Add text labels on top of each bar
    for i in range(len(adjust_d)):
        fig.add_annotation(
            x=adjust_d['QUERY_TAG'][i],
            y=adjust_d['CREDITS_USED_PER_USER_APROX'][i],
            text=str(round(adjust_d['CREDITS_USED_PER_USER_APROX'][i], 2)),
            font=dict(color='black', size=12),
            showarrow=False,
            xanchor='center',
            yanchor='bottom'
        )
    
    # Add total value
    fig.add_annotation(
    x=adjust_d['QUERY_TAG'].iloc[-1],
    y=total_credits,
    text=f'Total: {round(total_credits, 2)}',
    font=dict(color='black', size=16),
    showarrow=False,
    xanchor='right',
    yanchor='top'  # Change here
    )


    fig.update_layout(xaxis_title='QUERY_TAG', yaxis_title='CRÉDITOS COBRADOS', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


# get and show all row properties in the "exploded" node
def getShapeProps(row, cols, label, credits):
    row = row.asDict()
    
    row['CREDITS_USED_PER_USER_APROX'] = credits
    
    vals = ''
    for col in cols:
    #if col != displayCol:
      val = '&nbsp;' if col not in row or row[col] is None else str(row[col])
      vals += (f'\t\t<tr><td align="left"><font color="#000000">{col}&nbsp;</font></td>\n'
        + f'\t\t<td align="left"><font color="#000000">{val}</font></td></tr>\n')
        
    row['CREDITS_USED_PER_USER_APROX'] = credits
    
    return (f' [ label=<<table style="rounded" border="0" cellborder="1" cellspacing="0" cellpadding="1" width="40" height="40">\n' 
    + f'\t\t<tr><td align="center" colspan="2"><font color="#000000" font="25"><b>{label}</b></font></td></tr>\n'  
    + f'{vals}\t\t</table>> ]')


# Função para tratamento dos Datframes passado em getShape para credit_sum
def new_dfs_2_credit_sum(df, date, d_m):
    if d_m == 'd':
        if df['END_TIME'].dtype != 'object':
            df['END_TIME'] = df['END_TIME'].astype(str)
    
        df['END_TIME'] = pd.to_datetime(df['END_TIME'], format='%Y-%m-%d')
    
        date_to_filter = pd.to_datetime(date).strftime('%Y-%m-%d')
        df_filtered = df[df['END_TIME'].dt.strftime('%Y-%m-%d') == date_to_filter]
    
        adjust_d = df_filtered.pivot_table(index='QUERY_TAG', values='CREDITS_USED_PER_USER_APROX',  aggfunc='sum')
        #st.write(adjust_d)
        return adjust_d.reset_index(inplace=True)
    else:
        adjust_d = df.pivot_table(index='END_TIME', columns='QUERY_TAG', values='CREDITS_USED_PER_USER_APROX', aggfunc='sum')
        adjust_d.reset_index(inplace=True)
    
        date_to_filter = pd.to_datetime(date).strftime('%Y/%m')
        
        adjust_d['Total'] = adjust_d[['forecast_ml', 'forecast_transform', 'results']].sum(axis=1)
        st.write(adjust_d)
        return adjust_d['Total']
        
# Função para complementar o getShape(), como teria que realizar para a 
# soma de cada dia do Mês e o a soma total do Mês
def getShape_total_credits(label, sum_query_tag):
    total_credits = {}
    for index, row_sum in sum_query_tag.iterrows():
        total_credits[row_sum['QUERY_TAG']] = row_sum['CREDITS_USED_PER_USER_APROX']
    return total_credits.get(label, 0)

# add node (with label and eventual value, df)
def getShape(row, cols, fromCol, toCol, all, t, df, date_monitor, d_m):
    # Tratamento para passar o DF corretamento, com a data definida
    # new_dfs_2_credit_sum(df, date_monitor, 'm')
    sum_query_tag_d = credit_sum_d(df, 0)
    sum_query_tag_m = credit_sum_m(df, date_monitor)
    fromToCol = fromCol if fromCol != '' else toCol
    label = str(row[fromToCol])
    
    # Como ele sobreescrevia o valor de creditos
    if d_m == 'd':
        credits = getShape_total_credits(label, sum_query_tag_d)
    else:
        credits = getShape_total_credits(label, sum_query_tag_m)
    
    if all:
        display = getShapeProps(row, cols, label, credits)
    else:
        display = f' [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" FONT="50"><TR><TD align="center"><B>{label}</B></TD></TR><TR><TD align="center">Créditos: {round(credits, 2)}</TD></TR></TABLE>> ]'
    return f'\n\t{t}n{str(row[fromToCol])}{display};'

# returns a DOT graphviz chart
def makeGraph(rows, cols, fromCol, toCol, rev, all, df, date_monitor, d_m='d'):
  s = ""; t = ""
  if fromCol == '': return s

  for row in rows:
    s += getShape(row, cols, fromCol, toCol, all, t, df, date_monitor, d_m)
    
  # add links
  if fromCol != '' and toCol != '':
    added_links = set()  
    for row in rows:
      if not pd.isna(row[toCol]):
        link = (str(row[fromCol]), str(row[toCol])) if not rev else (str(row[toCol]), str(row[fromCol]))
        if link not in added_links:  
          added_links.add(link)
          s += f'\n\tn{link[0]} -> n{link[1]};'

  # add digraph around
  shape = 'Mrecord' #if valueCol == '' else 'circle'
  s = (f'digraph {{\n'
    + f'\tgraph [rankdir="LR"; compound="True" color="Gray"];\n'
    + f'\tnode [shape="{shape}" style="filled, rounded" color="lightgray"]'
    + f'{s}\n}}')
  return s

# allows Snowflake connection from the account or locally
def getSession():
  try:
    return get_active_session()
  except:
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
    section = "connections.my_conn"
    pars = {
      "account": parser.get(section, "accountname"),
      "user": parser.get(section, "username"),
      "password": parser.get(section, "password")
    }
    return Session.builder.configs(pars).create()

# get column names (and numeric-only column names)
def getColNames(cols, dtypes):
  colsN = []
  l = len(cols)
  for i in range(l):
    if str(dtypes[i]).startswith("int") or str(dtypes[i]).startswith("float64"):
      colsN.append(cols[i])
  cols.insert(0, "")
  colsN.insert(0, "")
  return tuple(cols), tuple(colsN)
   
# run the SQL query, when changed
@st.cache_resource(show_spinner="Executing the SQL query...")
def runQuery(query):
  res = getSession().sql(query)
  rows = res.collect()
  cols = res.columns
  # dtypes = pd.DataFrame(rows).dtypes.values
  # dtypes = pd.DataFrame(rows).astype({'CREDITS_USED_PER_USER_APROX':'float'}).dtypes.values
  dtypes = pd.DataFrame(getSession().sql(query).collect()).astype({'CREDITS_USED_PER_USER_APROX':'float'}).dtypes.values
  cols, colsN = getColNames(cols, dtypes)
  return rows, cols, colsN

def procces_filter(query, filters):
    dfs = [] 

    for filter in filters:
        filtered_df = query[query['QUERY_TAG'] == filter] 
        dfs.append(filtered_df)  
    concatenated_df = pd.concat(dfs, ignore_index=True) 
    return concatenated_df

def show_all_products(df):
  
    container1 = st.container()
    col1, col2 = container1.columns(2)
    
    n_tables = len(df['OBJ_NAME'].unique())

    # Preencher pelos dados da tabela
    with col1:
        title = df['TAG_NAME'].astype(str).unique()[0].replace('_', ' ')
        col1.title(f'{title}: ')
        col1.write(f'Owner: {df["OWNER"].unique()[0]}')
        col1.write(f'Quantidade de tabelas: {n_tables}')
        col1.write('Descrição: Previsão de vendas da loja X para os itens de jaqueta e guarda-chuva, com base no histórico de vendas e dados climáticos.')
        with col1.expander('Detalhes das informações do produto'):
            df = df[['TAG_VALUE', 'OBJ_NAME', 'REFRESH_VALUE']]
            df.columns = ['OJECT_TYPE', 'TABLE_NAME', 'REFRESH_VALUE']
            st.write(df.drop_duplicates().reset_index(drop=True))
            
    with col2:
        col2.title("Data Product 2: ")
        col2.write('Owner: -')
        col2.write('Quantidade de tabelas: -')
        col2.write('Descrição: -')
    container1.divider()

    st.write(df)

    
def show_data_product_1(query, rows, cols, df2):

    st.session_state["query"] = query

    dtypes = pd.DataFrame(query).astype({'CREDITS_USED_PER_USER_APROX':'float'}).dtypes.values
    cols, colsN = getColNames(cols, dtypes)
#   return rows, cols, colsN

    # rows, cols, colsN = runQuery(query)
    # st.write(rows)
    # df2 = pd.DataFrame(rows)

    new_entry = {
        'OWNER': 'MERCANTIL',
        'TAG_NAME': 'FORECAST_DATA_PRODUCT',
        'END_TIME': '2024-02-10',
        'SOURCE': 'forecast_ml',
        'QUERY_TAG': 'results',
        'REFRESH_VALUE': 'hourly',
        'CREDITS_USED_PER_USER_APROX': 0.8618
    }
    
    # Criando um DataFrame a partir da nova entrada
    new_row_df = pd.DataFrame([new_entry])
    
    # Concatenando o novo DataFrame com o DataFrame existente
    df2 = pd.concat([df2, new_row_df], ignore_index=True)

    df2['CREDITS_USED_PER_USER_APROX'] = df2['CREDITS_USED_PER_USER_APROX'].astype(float)

    #df = st.dataframe(df2, use_container_width=True)
    
    fromCol = 'QUERY_TAG'
    toCol = 'SOURCE'
    rev = True

    container0 = st.container()
    title = query['TAG_NAME'].astype(str).unique()[0].replace('_', ' ')
    container0.title(f'{title}:')
    container0.header('Monitoramento de Créditos Cobrados')
    container0.subheader('Data de monitoramento e processos: ')

    # Definindo min e max para o date_input
    df_aux = df2.copy()
    df_aux['END_TIME'] = pd.to_datetime(df_aux['END_TIME'])
    
    container1 = st.container()
    col1, col2 = container1.columns(2)
    min_date = df_aux['END_TIME'].min()
    max_date = df_aux['END_TIME'].max()

    col1.text('Processos que fazem parte do Data Product.')
    procces = col1.multiselect('Selecione o processo:', df2['QUERY_TAG'].unique(), df2['QUERY_TAG'].unique(), help='Selecione o processo para filtrar a tabela')
    col1.text('A data de monitoramento ao ser definida, mostrará o gasto diário e do mês da data \nselecionada.')
    monitoring_date = col1.date_input('Selecione a data de monitoramento:', datetime.date(2024, 2, 9), min_value=min_date, max_value=max_date, help='A partir da data selecionada, será mostrada o gasto diário e total do mês')
    container1.divider()
    if len(procces) != 0:
        df_selected_procces = procces_filter(df2, procces)
        sum_d = credit_sum_d(df_selected_procces, monitoring_date) 
        sum_m = credit_sum_m(df_selected_procces, monitoring_date)

        if selected_product in list_products:
            
            container2 = st.container()
            container2.subheader('Gastos do Data Product durante um Mês: ')
            
            col1, col2 = container2.columns(2)

            with col1:
                plot_credit_billed_day(sum_d, monitoring_date)
            with col2:
                plot_credit_billed_month(sum_m, monitoring_date)
            container2.divider()
            
            container3 = st.container()
            container3.subheader('Grafo e custos creditados de um dia: ')
            all = container3.checkbox('Expand All', help='Tp show all row values as shape properties')

            s = makeGraph(rows, cols, fromCol, toCol, rev, all, df2, monitoring_date, 'd')
            container3.graphviz_chart(s, use_container_width=True)

            container4 = st.container()
            container4.subheader('Grafo e custos creditados de um mês: ')
            all = container4.checkbox('Expand All', key=1, help='Tp show all row values as shape properties')

            s = makeGraph(rows, cols, fromCol, toCol, rev, all, df2, monitoring_date, 'm')
            container4.graphviz_chart(s, use_container_width=True)


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
    elif sub_tab == "Grafo":
        show_graph_content_dp2()

st.set_page_config(layout="wide")

list_products = ["Catálogo", "Forecast Data Product", "DataProduct 2", "DataProduct 3"]
# Organizando a apresentação do dataProduct
selected_product = st.sidebar.selectbox("Selecione um produto:", list_products)

query = "select owner, tag_name, obj_name, tag_value, end_time, source, query_tag, refresh_value, credits_used_per_user_aprox from upload_forecast_dp.ml_forecasting.FORECAST_PRODUCT_v2 order by query_tag;"
rows, cols, colsN = runQuery(query)
df = pd.DataFrame(rows)
#query = pd.read_csv('Custo detalhado.csv')


if selected_product == 'Catálogo':
    show_all_products(query)
elif selected_product == "Forecast Data Product":
    show_data_product_1(query, rows, cols, df)
elif selected_product == "DataProduct 2":
    show_data_product_2()
