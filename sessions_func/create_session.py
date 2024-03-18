from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
import os
import streamlit as st

import configparser  # Import the configparser module

def getSession():
    """_summary_

    Returns:
        conn: snowflake connection
    """
    conn = st.connection("snowflake")
    return conn

# def getSession():
#     parser = configparser.ConfigParser()
#     parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
#     section = "connections.my_conn"
#     pars = {
#         "account": parser.get(section, "accountname"),
#         "user": parser.get(section, "username"),
#         "password": parser.get(section, "password"),
#         "warehouse": parser.get(section, "warehouse"),
#         "database": parser.get(section, "dbname"),
#         "schema": parser.get(section, "schemaname"),
#         "role": parser.get(section, "rolename")
#     }
#     #st.write(pars)
#     return Session.builder.configs(pars).create()

@st.cache_resource(show_spinner="Executing the SQL query...")
def runQuery(query):
    """_summary_
    
    Args:
        query (str): SQL query

    Returns:
        dataframe: data from the query
    """
    session = getSession()
    #session.sql("use warehouse COMPUTE_WH")
    data = session.query(query)#.collect()
    return data

