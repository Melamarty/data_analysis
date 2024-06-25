import pandas as pd
from sqlalchemy import create_engine

def extract_data(csv_file):
    return pd.read_csv(csv_file)

def transform_data(df):
    df['time'] = df['time'].str.replace(' min', '')
    df['time'] = df['time'].str.replace(' season', '')
    df['time'] = df['time'].str.replace(' seasons', '')
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

def load_data(df, user, password, host, database):
    engine = get_mysql_engine(user, password, host, database)
    df.to_sql('netflix_titles', con=engine, if_exists='replace', index=False)

if __name__ == "__main__":
    # Example connection parameters
    user = 'root'
    password = 'simo'
    host = '127.0.0.1'
    database = 'simodb'

    df = extract_data('data.csv')
    df = transform_data(df)
    load_data(df, user, password, host, database)

