import pandas as pd
import plotly.express as px
import streamlit as st

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


def credit_billed_year(df, date):
    adjust_d = df.copy()

    adjust_d['END_TIME'] = pd.to_datetime(adjust_d['END_TIME'])
    
    year = pd.to_datetime(date).year
    adjust_d = adjust_d[adjust_d['END_TIME'].dt.year == year]

    adjust_d['MonthYear'] = adjust_d['END_TIME'].dt.strftime('%Y-%m') 

    adjust_d = adjust_d.groupby(['MonthYear', 'QUERY_TAG']).agg({'CREDITS_USED_PER_USER_APROX': 'sum'}).reset_index()

    # st.write(adjust_d)

    val_total = round(adjust_d["CREDITS_USED_PER_USER_APROX"].sum(), 2)

    return adjust_d, year, val_total


def credit_billed_month(df, date):
    adjust_d = df.pivot_table(index='END_TIME', columns='QUERY_TAG', values='CREDITS_USED_PER_USER_APROX', aggfunc='sum')
    adjust_d.reset_index(inplace=True)

    # Convert 'END_TIME' to date format
    adjust_d['END_TIME'] = pd.to_datetime(adjust_d['END_TIME']).dt.date
    
    date_to_filter = pd.to_datetime(date).strftime('%Y/%m')
    
    adjust_d['Total'] = adjust_d[df['QUERY_TAG'].unique()].sum(axis=1)
    total_credits = adjust_d['Total'].sum()

    return adjust_d, date_to_filter, round(total_credits, 2)


def credit_billed_day(df, date):
    if df['END_TIME'].dtype != 'object':
        df['END_TIME'] = df['END_TIME'].astype(str)

    df['END_TIME'] = pd.to_datetime(df['END_TIME'], format='%Y-%m-%d')

    date_to_filter = pd.to_datetime(date).strftime('%Y/%m/%d')
    df_filtered = df[df['END_TIME'].dt.strftime('%Y/%m/%d') == date_to_filter]

    adjust_d = df_filtered.pivot_table(index='QUERY_TAG', values='CREDITS_USED_PER_USER_APROX',  aggfunc='sum')
    adjust_d.reset_index(inplace=True)

    total_credits = adjust_d['CREDITS_USED_PER_USER_APROX'].sum()  

    return adjust_d, date_to_filter, round(total_credits,2)

def plot_credit_billed_year(df, date, container):
    colors = ['#249edc', '#005b96', '#b3cde0']
    adjust_d, year, _ = credit_billed_year(df, date)
                      
    unique_tags = df['QUERY_TAG'].unique()
    num_unique_tags = len(unique_tags)
    if colors is None:
        colors = px.colors.qualitative.Set1[:num_unique_tags]
    color_map = dict(zip(unique_tags, colors))

    fig = px.bar(adjust_d, x='MonthYear', y='CREDITS_USED_PER_USER_APROX', 
                 color='QUERY_TAG', color_discrete_map=color_map,
                 labels={'MonthYear': 'Mês e Ano', 'CREDITS_USED_PER_USER_APROX': 'Créditos Cobrados'},
                 text_auto=True)
    fig.update_xaxes(type='category')

    fig.add_annotation(x=adjust_d['MonthYear'].iloc[-1], y='CREDITS_USED_PER_USER_APROX',
                       text='',
                       showarrow=False,
                       font=dict(color='black', size=16),
                       xanchor='center', yanchor='bottom')

    container.subheader(f'Créditos cobrados em {year}')
    fig.update_layout(xaxis_title='Mês e Ano', yaxis_title='Créditos Cobrados')
    st.plotly_chart(fig, use_container_width=True)


def plot_credit_billed_month(df, date, col2):
    colors = ['#249edc', '#005b96', '#b3cde0']
    adjust_d, date_to_filter, total_credits = credit_billed_month(df, date)

    # Definindo cores automaticamente com base nas tags únicas
    unique_tags = df['QUERY_TAG'].unique()
    num_unique_tags = len(unique_tags)
    if colors is None:
        colors = px.colors.qualitative.Set1[:num_unique_tags]
    color_map = dict(zip(unique_tags, colors))

    # Plotting with Plotly
    fig = px.bar(adjust_d, x='END_TIME', y=df['QUERY_TAG'],
                 title=f'Créditos gastos em {date_to_filter}',
                 color_discrete_map=color_map)

    fig.update_xaxes(type='category')

    # Add total value annotation
    fig.add_annotation(x=adjust_d['END_TIME'].iloc[-1], y=total_credits,
                       text=f'Total: {round(total_credits, 2)}',
                       showarrow=False,
                       font=dict(color='black', size=16),
                       xanchor='center', yanchor='bottom')

    col2.subheader(f'Créditos cobrados em {date_to_filter}')
    fig.update_layout(xaxis_title='DATA', yaxis_title='CRÉDITOS COBRADOS', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


# Plot dos gráficos usando o st.bar_chart
def plot_credit_billed_day(df, date, col1):
    adjust_d, date_to_filter, total_credits = credit_billed_day(df, date)

    fig = px.bar(adjust_d, x='QUERY_TAG', y='CREDITS_USED_PER_USER_APROX'
                 ,color_discrete_sequence=['#249edc'])
    
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
    yanchor='top' 
    )

    col1.subheader(f'Créditos cobrados em {date_to_filter}')
    fig.update_layout(xaxis_title='PROCESSOS', yaxis_title='CRÉDITOS COBRADOS')
    st.plotly_chart(fig, use_container_width=True)
