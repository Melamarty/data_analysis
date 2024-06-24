import pandas as pd
import sqlite3

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

def load_data(df, db_file):
    conn = sqlite3.connect(db_file)
    df.to_sql('netflix_titles', conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    df = extract_data('data.csv')
    df = transform_data(df)
    load_data(df, 'db_netflix.sqlite')
