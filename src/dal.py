import sqlite3

def get_connection(db_file):
    return sqlite3.connect(db_file)

def execute_query(query, db_file):
    conn = get_connection(db_file)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result
