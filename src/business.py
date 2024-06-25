import matplotlib.pyplot as plt
import pandas as pd
from dal import execute_query

# MySQL connection parameters
USER = 'root'
PASSWORD = 'simo'
HOST = '127.0.0.1'
DATABASE = 'simodb'

def plot_movies_by_country():
    query = "SELECT country, COUNT(*) as count FROM netflix_titles WHERE type='Movie' GROUP BY country"
    result = execute_query(query, USER, PASSWORD, HOST, DATABASE)
    df = pd.DataFrame(result, columns=['Country', 'Count'])
    df.plot(kind='bar', x='Country', y='Count')
    plt.title('Number of Movies by Country')
    plt.savefig('output/movies_by_country.png')

def plot_shows_and_movies_by_year_range():
    query = """SELECT year_range, type, COUNT(*) as count FROM netflix_titles
               WHERE year_range IS NOT NULL
               GROUP BY year_range, type"""
    result = execute_query(query, USER, PASSWORD, HOST, DATABASE)
    df = pd.DataFrame(result, columns=['Year Range', 'Type', 'Count'])
    pivot_df = df.pivot(index='Year Range', columns='Type', values='Count')
    pivot_df.plot(kind='bar')
    plt.title('TV Shows and Movies by Year Range')
    plt.savefig('output/shows_movies_by_year_range.png')

def plot_movies_by_duration():
    query = """SELECT CASE
               WHEN time < 90 THEN '< 90 min'
               WHEN time BETWEEN 90 AND 120 THEN '90 - 120 min'
               ELSE '> 120 min' END as duration, COUNT(*) as count
               FROM netflix_titles WHERE type='Movie'
               GROUP BY duration"""
    result = execute_query(query, USER, PASSWORD, HOST, DATABASE)
    df = pd.DataFrame(result, columns=['Duration', 'Count'])
    df.plot(kind='pie', y='Count', labels=df['Duration'], autopct='%1.1f%%')
    plt.title('Movies by Duration')
    plt.ylabel('')
    plt.savefig('output/movies_by_duration.png')

def plot_shows_by_season():
    query = """SELECT CASE
               WHEN time = 1 THEN '1 season'
               WHEN time BETWEEN 2 AND 3 THEN '2-3 seasons'
               ELSE '> 3 seasons' END as seasons, COUNT(*) as count
               FROM netflix_titles WHERE type='TV Show'
               GROUP BY seasons"""
    result = execute_query(query, USER, PASSWORD, HOST, DATABASE)
    df = pd.DataFrame(result, columns=['Seasons', 'Count'])
    df.plot(kind='pie', y='Count', labels=df['Seasons'], autopct='%1.1f%%')
    plt.title('TV Shows by Season')
    plt.ylabel('')
    plt.savefig('output/shows_by_season.png')

if __name__ == "__main__":
    plot_movies_by_country()
    plot_shows_and_movies_by_year_range()
    plot_movies_by_duration()
    plot_shows_by_season()
