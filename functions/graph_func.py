from graphviz import Digraph
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
from streamlit_modal import Modal
import streamlit.components.v1 as components
import streamlit as st


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
            f"<tr><td align='left'><font size='500'>Créditos cobrados</font></td><td align='left'>{row['CREDITS_USED_PER_USER_APROX']}</td></tr>"
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

def pop_up_graph():
   pass
    

def make_agraph():
    modal = Modal(
        "Demo Modal", 
        key="demo-modal",
        
        # Optional
        padding=20,    # default value
        max_width=744  # default value
    )
    open_modal = st.button("Open")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            st.write("Text goes here")

            html_string = '''
            <h1>HTML string in RED</h1>

            <script language="javascript">
            document.querySelector("h1").style.color = "red";
            </script>
            '''
            components.html(html_string)
    
    nodes = []
    edges = []
    nodes.append( Node(id="Spiderman",
                    title=st.button("Open", key=80),
                    label="Peter Parker", 
                    size=25, 
                    shape="circularImage",
                    image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png") 
                ) # includes **kwargs
    nodes.append( Node(id="Captain_Marvel", 
                    size=25,
                    shape="circularImage",
                    image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png") 
                )
    edges.append( Edge(source="Captain_Marvel", 
                    label="friend_of", 
                    target="Spiderman", 
                    # **kwargs
                    ) 
                ) 

    config = Config(width=750,
                    height=950,
                    directed=True, 
                    physics=True, 
                    hierarchical=False,
                    # **kwargs
                    )

    return_value = agraph(nodes=nodes, 
                        edges=edges, 
                        config=config)
   