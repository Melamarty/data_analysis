import mysql.connector
import pandas as pd

def get_mysql_connection(user, password, host, database):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

def execute_query(query, user, password, host, database):
    conn = get_mysql_connection(user, password, host, database)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
