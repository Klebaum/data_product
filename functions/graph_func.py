from graphviz import Digraph

def make_graph(df):
    """_summary_

    Args:
        df (DataFrame): dataframe to be used in the graph.

    Returns:
        graphviz element: graphviz element with the graph.
    """
    dot = Digraph(graph_attr={'rankdir': 'LR', 'bgcolor': '#ffffff'})

    df_graph = df.groupby(['QUERY_TAG', 'SOURCE', 'REFRESH_VALUE']).agg({
        'CREDITS_USED_PER_USER_APROX': 'sum',
        'TAG_VALUE': lambda x: ', '.join(set(x))
    }).reset_index()

    for index, row in df_graph.iterrows():
        label_query = (
            f"<"
            f"<table border='0' cellborder='0' cellspacing='0'>"
            f"<tr><td colspan='2'><b>{row['QUERY_TAG']}</b></td></tr>"
            f"<tr><td align='left'><font size='500'>Créditos cobrados</font></td><td align='left'>{round(row['CREDITS_USED_PER_USER_APROX'], 3)}</td></tr>"
            f"<tr><td align='left'>Tipo dos Objetos</td><td align='left'>{row['TAG_VALUE']}</td></tr>"
            f"<tr><td align='left'>Refresh</td><td align='left'>{row['REFRESH_VALUE']}</td></tr>"
            f"</table>"
            f">"
        )
        dot.node(row['SOURCE'], shape='rectangle',style='rounded', color='#249edc', fontsize='20')
        dot.node(row['QUERY_TAG'], label=label_query, shape='rectangle', style='rounded', color='#249edc', fontsize='20')
    
    for index, row in df_graph.iterrows():
        dot.edge(row['SOURCE'], row['QUERY_TAG'])

    return dot
