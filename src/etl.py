import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def extract_data(csv_file):
    return pd.read_csv(csv_file)

def transform_data(df):
    df['time'] = df['time'].str.replace(' min', '')
    df['time'] = df['time'].str.replace(' Season', '')
    df['time'] = df['time'].str.replace(' Seasons', '')
    df['time'] = pd.to_numeric(df['time'], errors='coerce')
    
    conditions = [
        (df['year'] >= 2015) & (df['year'] <= 2019),
        (df['year'] > 2019) & (df['year'] <= 2023)
    ]
    choices = ['2015-2019', '2019-2023']
    df['year_range'] = pd.cut(df['year'], bins=[2014, 2019, 2023], labels=choices, include_lowest=True)
    
    return df

def get_mysql_engine(user, password, host, database):
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
    return engine

def load_data(df, user, password, host, database, chunksize=1000):
    engine = get_mysql_engine(user, password, host, database)
    try:
        with engine.connect() as connection:
            df.to_sql('netflix_titles', con=connection, if_exists='replace', index=False, chunksize=chunksize)
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    # Example connection parameters
    user = 'root'
    password = 'simo'
    host = '127.0.0.1'
    database = 'simodb'

    df = extract_data('netflix.csv')
    df = transform_data(df)
    load_data(df, user, password, host, database)
