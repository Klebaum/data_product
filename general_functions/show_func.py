import pandas as pd
import streamlit as st
import datetime
import plotly.express as px

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

def credit_sum_total(df, var_to_group='TAG_NAME'):
    df = df.groupby(var_to_group)['CREDITS_USED_PER_USER_APROX'].sum().reset_index()
    return df

def ranking_plot(df, col1, mult_rank, var_to_group='TAG_NAME'):
    adjust_d = credit_sum_total(df, var_to_group)
    adjust_d = adjust_d.sort_values(by='CREDITS_USED_PER_USER_APROX', ascending=True)

    fig = px.bar(adjust_d, y=var_to_group, x='CREDITS_USED_PER_USER_APROX'
                 ,color_discrete_sequence=['#249edc'], orientation='h')
    
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
    
    col1.subheader(f'Produtos que mais consomem créditos')
    fig.update_layout(xaxis_title='CRÉDITOS COBRADOS', yaxis_title='PRODUTOS')
    col1.plotly_chart(fig, use_container_width=True)

def pie_plot(df, col1, mult_pie, var_to_group='TAG_NAME'):
    colors = ['#249edc', '#005b96', '#b3cde0']
   
    adjust_d = credit_sum_total(df, var_to_group)

    unique_tags = adjust_d[var_to_group].unique()
    num_unique_tags = len(unique_tags)
    if colors is None:
        colors = px.colors.qualitative.Set1[:num_unique_tags]
    color_map = dict(zip(unique_tags, colors))

    fig = px.pie(adjust_d, values='CREDITS_USED_PER_USER_APROX', names=var_to_group 
                ,color=var_to_group, color_discrete_map=color_map)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(width=600, height=500)
    st.subheader('Porcentagem de consumo de créditos')
    st.plotly_chart(fig, use_container_width=True)