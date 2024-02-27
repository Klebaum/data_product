import pandas as pd
from functions.show_products import show_data_product_1
query = pd.read_csv('Custo detalhado.csv')
show_data_product_1(query)
