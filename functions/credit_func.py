import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
pd.options.mode.chained_assignment = None  # default='warn'

def credit_sum_y(df, date_m, var_to_group='QUERY_TAG'):
    """_summary_
    
    Args:
        df (DataFrame): dataframe with the data to be used in the analysis.
        date_m (datetime.date): date to be used in the analysis.

    Returns:
        DataFrame: dataframe with the yearly sum of credits billed.
    """
    df2 = df.copy()
    df2['END_TIME'] = pd.to_datetime(df2['END_TIME'])
    df2['END_TIME'] = df2['END_TIME'].dt.to_period('Y').astype(str)
    year_sum = df2.groupby(['END_TIME', 'QUERY_TAG', 'TAG_NAME'])['CREDITS_USED_PER_USER_APROX'].sum().reset_index()
    date_year = pd.to_datetime(date_m).strftime('%Y')
    year_sum['END_TIME'] = year_sum['END_TIME'].astype(str)
    year_sum_filtered = year_sum[year_sum['END_TIME'].str.startswith(date_year)]

    return year_sum_filtered

def credit_sum_m(df, date_m):
    """_summary_

    Args:
        df (DataFrame): dataframe with the data to be used in the analysis.
        date_m (datetime.date): date to be used in the analysis.

    Returns:
        DataFrame: dataframe with the monthly sum of credits billed.
    """
    df2 = df.copy()
    df2['END_TIME'] = pd.to_datetime(df2['END_TIME'])
    df2['END_TIME'] = df2['END_TIME'].dt.to_period('D').astype(str)
    monthly_sum = df2.groupby(['END_TIME', 'QUERY_TAG', 'TAG_NAME'])['CREDITS_USED_PER_USER_APROX'].sum().reset_index()
    date_m_month_year = pd.to_datetime(date_m).strftime('%Y-%m')
    monthly_sum['END_TIME'] = monthly_sum['END_TIME'].astype(str)
    monthly_sum_filtered = monthly_sum[monthly_sum['END_TIME'].str.startswith(date_m_month_year)]

    return monthly_sum_filtered


def credit_sum_d(df, date_m):
    """_summary_

    Args:
        df (DataFrame): dataframe with the data to be used in the analysis.
        date_m (datetime.date): date to be used in the analysis.

    Returns:
        DataFrame: dataframe with the daily sum of credits billed.
    """
    # df2 = df.copy()
    # df2['END_TIME'] = pd.to_datetime(df2['END_TIME'])
    # daily_sum = df2.groupby([df2['END_TIME'].dt.date, 'QUERY_TAG', 'TAG_NAME'])['CREDITS_USED_PER_USER_APROX'].sum().reset_index()
    
    df2 = df.copy()
    df2['END_TIME'] = pd.to_datetime(df2['END_TIME'])
    df2['END_TIME'] = df2['END_TIME'].dt.to_period('D').astype(str)
    monthly_sum = df2.groupby(['END_TIME', 'QUERY_TAG', 'TAG_NAME'])['CREDITS_USED_PER_USER_APROX'].sum().reset_index()
    date_m_month_year = pd.to_datetime(date_m).strftime('%Y-%m-%d')
    monthly_sum['END_TIME'] = monthly_sum['END_TIME'].astype(str)
    daily_sum = monthly_sum[monthly_sum['END_TIME'].str.startswith(date_m_month_year)]

    return daily_sum


def credit_billed_year(df, date, var_to_group='QUERY_TAG'):
    """_summary_

    Args:
        df (DataFrame): dataframe with the data to be used in the analysis.
        date (datetime.date): date to be used in the analysis.
        var_to_group (str, optional): variable to group the data. Defaults to 'QUERY_TAG'.

    Returns:
        DataFrame: dataframe with the credits billed in the year.
        str: year with the format 'YYYY'.
        float: total of credits billed in the year.
    """
    adjust_d = df.copy()

    adjust_d['END_TIME'] = pd.to_datetime(adjust_d['END_TIME'])
    
    year = pd.to_datetime(date).year
    adjust_d = adjust_d[adjust_d['END_TIME'].dt.year == year]

    adjust_d['MonthYear'] = adjust_d['END_TIME'].dt.strftime('%Y-%m') 

    adjust_d = adjust_d.groupby(['MonthYear', var_to_group]).agg({'CREDITS_USED_PER_USER_APROX': 'sum'}).reset_index()

    # st.write(adjust_d)

    val_total = round(adjust_d["CREDITS_USED_PER_USER_APROX"].sum(), 2)

    return adjust_d, year, val_total


def credit_billed_month(df, date, var_to_group='QUERY_TAG'):
    """_summary_
    
    Args:
        df (DataFrame): dataframe with the data to be used in the analysis.
        date (datetime.date): date to be used in the analysis.
        var_to_group (str, optional): variable to group the data. Defaults to 'QUERY_TAG'.

    Returns:
        DataFrame: dataframe with the credits billed in the month.
        str: date with the format 'YYYY/MM'.
        float: total of credits billed in the month. 
    """
    
    # adjust_d = df.pivot_table(index='END_TIME', columns=var_to_group, values='CREDITS_USED_PER_USER_APROX', aggfunc='sum')
    # adjust_d.reset_index(inplace=True)

    # # Convert 'END_TIME' to date format
    # adjust_d['END_TIME'] = pd.to_datetime(adjust_d['END_TIME']).dt.date
    
    # date_to_filter = pd.to_datetime(date).strftime('%Y/%m')
    
    # adjust_d['Total'] = adjust_d[df[var_to_group].unique()].sum(axis=1)
    # total_credits = adjust_d['Total'].sum()

    # return adjust_d, date_to_filter, round(total_credits, 2)

    adjust_d = df.copy()

    adjust_d['END_TIME'] = pd.to_datetime(adjust_d['END_TIME'])
    
    date_to_filter = pd.to_datetime(date).strftime('%Y/%m')
    year = pd.to_datetime(date).year
    adjust_d = adjust_d[adjust_d['END_TIME'].dt.year == year]

    adjust_d['Day'] = adjust_d['END_TIME'].dt.strftime('%Y-%m-%d') 

    adjust_d = adjust_d.groupby(['Day', var_to_group]).agg({'CREDITS_USED_PER_USER_APROX': 'sum'}).reset_index()

    # st.write(adjust_d)

    val_total = round(adjust_d["CREDITS_USED_PER_USER_APROX"].sum(), 2)

    return adjust_d, date_to_filter, val_total


def credit_billed_day(df, date, var_to_group='QUERY_TAG'):
    """_summary_
    
    Args:
        df (DataFrame): dataframe with the data to be used in the analysis.
        date (datetime.date): date to be used in the analysis.
        var_to_group (str, optional): variable to group the data. Defaults to 'QUERY_TAG'.

    Returns:
        DataFrame: dataframe with the credits billed in the day.
        str: date with the format 'YYYY/MM/DD'.
        float: total of credits billed in the day.
    """
    if df['END_TIME'].dtype != 'object':
        df['END_TIME'] = df['END_TIME'].astype(str)

    df['END_TIME'] = pd.to_datetime(df['END_TIME'], format='%Y-%m-%d')

    date_to_filter = pd.to_datetime(date).strftime('%Y/%m/%d')
    df_filtered = df[df['END_TIME'].dt.strftime('%Y/%m/%d') == date_to_filter]

    adjust_d = df_filtered.pivot_table(index=var_to_group, values='CREDITS_USED_PER_USER_APROX',  aggfunc='sum')
    adjust_d.reset_index(inplace=True)

    if adjust_d.empty:
        return adjust_d, date_to_filter, 0.0
    total_credits = adjust_d['CREDITS_USED_PER_USER_APROX'].sum()  

    return adjust_d, date_to_filter, round(total_credits,2)


def plot_credit_billed_year(df, date, container, var_to_group='QUERY_TAG'):
    """_summary_
    
    Args:
        df (DataFrame): dataframe with the data to be used in the analysis.
        date (datetime.date): date to be used in the analysis.
        container (streamlit.container): container to plot the graph.
        var_to_group (str, optional): variable to group the data. Defaults to 'QUERY_TAG'.

    Returns:
        None: plot the chart bar graph with the credits billed in the year.
    """
    colors = ['#249edc', '#005b96', '#b3cde0']
    adjust_d, year, _ = credit_billed_year(df, date, var_to_group)
                      
    unique_tags = df[var_to_group].unique()
    num_unique_tags = len(unique_tags)
    if colors is None:
        colors = px.colors.qualitative.Set1[:num_unique_tags]
    color_map = dict(zip(unique_tags, colors))

    fig = px.bar(adjust_d, x='MonthYear', y='CREDITS_USED_PER_USER_APROX', 
                 color=var_to_group, color_discrete_map=color_map,
                 labels={'MonthYear': 'Mês e Ano', 'CREDITS_USED_PER_USER_APROX': 'Créditos Cobrados'},
                 width=500, height=250
                )
    fig.update_xaxes(type='category')

    fig.add_annotation(x=adjust_d['MonthYear'].iloc[-1], y='CREDITS_USED_PER_USER_APROX',
                       text='',
                       showarrow=False,
                       font=dict(color='black', size=10),
                       xanchor='center', yanchor='bottom')

    container.markdown(f'<p style="color:#3d3d3c; font-family:Source Sans Pro, sans serif; font-size: 20px;"><b>Créditos cobrados em {year}</b></p>', unsafe_allow_html=True)
    fig.update_layout(xaxis_title='MÊS E ANO', yaxis_title='CRÉDITOS COBRADOS')
    container.plotly_chart(fig, use_container_width=True)


def plot_credit_billed_month(df, date, col2, var_to_group='QUERY_TAG'):
    """_summary_
    
    Args:
        df (DataFrame): dataframe with the data to be used in the analysis.
        date (datetime.date): date to be used in the analysis.
        col2 (streamlit.container): container to plot the graph.
        var_to_group (str, optional): variable to group the data. Defaults to 'QUERY_TAG'.

    Returns:
        None: plot the chart bar graph with the credits billed in the month.
    
    """
    colors = ['#249edc', '#005b96', '#b3cde0']
    adjust_d, date_to_filter, total_credits = credit_billed_month(df, date, var_to_group)

    # Definindo cores automaticamente com base nas tags únicas
    unique_tags = df[var_to_group].unique()
    num_unique_tags = len(unique_tags)
    if colors is None:
        colors = px.colors.qualitative.Set1[:num_unique_tags]
    color_map = dict(zip(unique_tags, colors))


    # Plotting with Plotly
    fig = px.line(adjust_d, x='Day', y='CREDITS_USED_PER_USER_APROX', markers=True, color=var_to_group, 
                color_discrete_map=color_map, width=500, height=250, 
                labels={'Day': 'Dia', 'CREDITS_USED_PER_USER_APROX': 'Créditos Cobrados'})
    
    fig.update_xaxes(type='category')

    # Add total value annotation
    # fig.add_annotation(x=adjust_d['Day'].iloc[-1], y=total_credits,
    #                    text='',
    #                    showarrow=False,
    #                    font=dict(color='black', size=16),
    #                    xanchor='center', yanchor='bottom')

    col2.markdown(f'<p style="color:#3d3d3c; font-family:Source Sans Pro, sans serif; font-size: 20px;"><b>Créditos cobrados em {date_to_filter}</b></p>', unsafe_allow_html=True)
    fig.update_layout(xaxis_title='DATA', yaxis_title='CRÉDITOS COBRADOS')
    st.plotly_chart(fig, use_container_width=True)


# Plot dos gráficos usando o st.bar_chart
def plot_credit_billed_day(df, date, col1, var_to_group='QUERY_TAG'):
    """_summary_
    
    Args:
        df (DataFrame): dataframe with the data to be used in the analysis.
        date (datetime.date): date to be used in the analysis.
        col1 (streamlit.container): container to plot the graph.
        var_to_group (str, optional): variable to group the data. Defaults to 'QUERY_TAG'.

    Returns:
        None: plot the chart bar graph with the credits billed in the day.
    """
    adjust_d, date_to_filter, total_credits = credit_billed_day(df, date, var_to_group)

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

    col1.markdown(f'<p style="color:#3d3d3c; font-family:Source Sans Pro, sans serif; font-size: 20px;"><b>Créditos cobrados em {date_to_filter}</b></p>', unsafe_allow_html=True)
    fig.update_layout(xaxis_title='PROCESSOS', yaxis_title='CRÉDITOS COBRADOS')
    st.plotly_chart(fig, use_container_width=True)
