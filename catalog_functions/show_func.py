import streamlit as st
import plotly.express as px

def score_card_geral(query, col2, daily_credits, monthly_credits, yearly_credits):
    """_summary_
    
    Args:
        query (DataFrame): DataFrame with the data to be used in the analysis.
        col2 (streamlit.container): Streamlit container to be used in the analysis.
        daily_credits (float): daily credits to be used in the analysis.
        monthly_credits (float): monthly credits to be used in the analysis.
        yearly_credits (float): yearly credits to be used in the analysis.

    Returns:
        None: return all the score cards.
    """
    

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
                 
        btc_col, eth_col, xmr_col, outros_col = st.columns([0.3,0.3,0.3,0.36], gap="small")
        with btc_col:
            with st.container(border=True):
                st.markdown(f'<p class="btc_text">ANUAL<br></p><p class="price_details">{yearly_credits}</p>', unsafe_allow_html = True)

        with eth_col:
            with st.container(border=True):
                st.markdown(f'<p class="eth_text">MENSAL<br></p><p class="price_details">{monthly_credits}</p>', unsafe_allow_html = True)

        with xmr_col:
            with st.container(border=True):
                st.markdown(f'<p class="xmr_text">DIÁRIO<br></p><p class="price_details">{daily_credits}</p>', unsafe_allow_html = True)

        with outros_col:
            with st.container(border=True):
                st.markdown(f'<p class="outros_text">OUTROS<br></p><p class="price_details">{60.0}</p>', unsafe_allow_html = True, help='Produtos não tageados.')

def credit_sum_total(df, var_to_group='TAG_NAME'):
    """_summary_
    
    Args:
        df (DataFrame): DataFrame with the data to be used in the analysis.
        var_to_group (str): variable to be used in the analysis.

    Returns:
        DataFrame: return the sum of the credits billed for all the products.
    """
    df = df.groupby(var_to_group)['CREDITS_USED_PER_USER_APROX'].sum().reset_index()
    return df


def ranking_plot(df, col1, var_to_group='TAG_NAME'):
    """_summary_
    
    Args:
        df (DataFrame): DataFrame with the data to be used in the analysis.
        col1 (streamlit.container): Streamlit container to be used in the analysis.
        var_to_group (str): variable to be used in the analysis.

    Returns:
        None: return the ranking plot.
    """
    adjust_d = credit_sum_total(df, var_to_group)
    adjust_d = adjust_d.sort_values(by='CREDITS_USED_PER_USER_APROX', ascending=True)

    fig = px.bar(adjust_d, y=var_to_group, x='CREDITS_USED_PER_USER_APROX'
                 ,color_discrete_sequence=['#249edc'], orientation='h', width=600, height=300)
    
    for i in range(len(adjust_d)):
        fig.add_annotation(
            x=adjust_d['CREDITS_USED_PER_USER_APROX'][i],
            y=adjust_d[var_to_group][i],
            text=str(round(adjust_d['CREDITS_USED_PER_USER_APROX'][i], 2)),
            font=dict(color='black', size=12),
            showarrow=False,
            xanchor='left',
            yanchor='middle'
        )
    
    col1.markdown(f'<p style="color:#3d3d3c; font-family:Source Sans Pro, sans serif; font-size: 20px;"><b>Produtos que mais consomem créditos</b></p>', unsafe_allow_html=True)
    fig.update_layout(xaxis_title='CRÉDITOS COBRADOS', yaxis_title='PRODUTOS')
    col1.plotly_chart(fig, use_container_width=True)
