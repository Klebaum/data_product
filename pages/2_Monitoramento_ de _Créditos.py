import pandas as pd
import streamlit as st
from functions.show_products import show_data_product_1
query = pd.read_csv('Custo detalhado.csv')

st.title('PRODUTOS DO CATÁLOGO')
st.selectbox('Selecione o produto: ', query['TAG_NAME'].unique(), help='Selecione o produto para visualizar os detalhes.')

show_data_product_1(query)
