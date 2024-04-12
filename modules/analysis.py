import pandas as pd
import matplotlib.pyplot as plt
from config import settings
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")


def load_movies_from_db(conn):
    return pd.read_sql_query("SELECT * FROM movies", conn)


def load_genres_from_db(conn):
    return pd.read_sql_query("SELECT * FROM genres", conn)


def plot_genre_distribution(movies_df_orig, genres_df):
    movies_df = movies_df_orig.copy()
    # Convert 'genre_ids' from string representation of list to actual list
    movies_df['genre_ids'] = movies_df['genre_ids'].str.strip('[]').str.split(',')

    # Split 'genre_ids' into separate rows
    movies_df = movies_df.explode('genre_ids')

    # Remove any leading/trailing spaces and convert 'genre_ids' to int64
    movies_df['genre_ids'] = movies_df['genre_ids'].str.strip().astype('int64')

    # Now perform the merge
    merged_df = movies_df.merge(genres_df, left_on='genre_ids', right_on='id', how='inner')

    # Plot the distribution of movie genres
    plt.figure(figsize=(10, 6))
    sns.countplot(data=merged_df, y='name')
    plt.title('Distribution of Movie Genres', fontsize=16, fontweight='bold')
    plt.xlabel('Count', fontsize=14)
    plt.ylabel('Genre', fontsize=14)
    plt.show()


def plot_release_year_distribution(movies_df):
    # Convert release_date to datetime and extract the year
    movies_df['release_year'] = pd.to_datetime(movies_df['release_date']).dt.year

    # Plot the distribution of movie release years
    plt.figure(figsize=(10, 6))
    sns.histplot(data=movies_df, x='release_year', bins=30)
    plt.title('Distribution of Movie Release Years', fontsize=16, fontweight='bold')
    plt.xlabel('Release Year', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.show()


def plot_average_popularity_by_genre(movies_df_orig, genres_df):
    movies_df = movies_df_orig.copy()
    # Convert 'genre_ids' from string representation of list to actual list
    movies_df['genre_ids'] = movies_df['genre_ids'].str.strip('[]').str.split(',')

    # Split 'genre_ids' into separate rows
    movies_df = movies_df.explode('genre_ids')

    # Remove any leading/trailing spaces and convert 'genre_ids' to int64
    movies_df['genre_ids'] = movies_df['genre_ids'].str.strip().astype('int64')
    # Merge the movies and genres dataframes
    merged_df = movies_df.merge(genres_df, left_on='genre_ids', right_on='id', how='inner')

    # Convert 'popularity' to float64
    merged_df['popularity'] = merged_df['popularity'].astype('float64')

    # Calculate the average popularity by genre
    avg_popularity = merged_df.groupby('name')['popularity'].mean().sort_values(ascending=False)
    # round to 2 decimal places
    avg_popularity = avg_popularity.round(2)

    # Plot the average popularity by genre
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_popularity.values, y=avg_popularity.index)
    plt.title('Average Popularity by Genre', fontsize=16, fontweight='bold')
    plt.xlabel('Average Popularity', fontsize=14)
    plt.ylabel('Genre', fontsize=14)
    plt.show()


def plot_average_vote_count_by_genre(movies_df_orig, genres_df):
    movies_df = movies_df_orig.copy()
    # Convert 'genre_ids' from string representation of list to actual list
    movies_df['genre_ids'] = movies_df['genre_ids'].str.strip('[]').str.split(',')

    # Split 'genre_ids' into separate rows
    movies_df = movies_df.explode('genre_ids')

    # Remove any leading/trailing spaces and convert 'genre_ids' to int64
    movies_df['genre_ids'] = movies_df['genre_ids'].str.strip().astype('int64')
    # Merge the movies and genres dataframes
    merged_df = movies_df.merge(genres_df, left_on='genre_ids', right_on='id', how='inner')

    # Convert 'popularity' to float64
    merged_df['vote_count'] = merged_df['vote_count'].astype('int16')

    # Calculate the average vote count by genre
    avg_vote_count = merged_df.groupby('name')['vote_count'].mean().sort_values(ascending=False)

    # Plot the average vote count by genre
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_vote_count.values, y=avg_vote_count.index)
    plt.title('Average Vote Count by Genre', fontsize=16, fontweight='bold')
    plt.xlabel('Average Vote Count', fontsize=14)
    plt.ylabel('Genre', fontsize=14)
    plt.show()


def plot_average_rating_by_genre(rows):
    genre_ratings = rows.groupby('genre_names')['vote_average'].mean()
    genre_ratings.sort_values(ascending=False).plot(kind='bar', color='skyblue')
    plt.title('Average Movie Rating by Genre', fontsize=16, fontweight='bold')
    plt.xlabel('Genre', fontsize=14)
    plt.ylabel('Average Rating', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_movies_over_time(movies_df):
    movies_df['release_year'] = pd.to_datetime(movies_df['release_date']).dt.year
    movies_per_year = movies_df.groupby('release_year').size()
    movies_per_year.plot(kind='line')
    plt.title('Number of Movies Released Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Movies', fontsize=14)
    plt.show()


def plot_actor_appearances(cast_df):
    actor_appearances = cast_df['actor_name'].value_counts().head(10)
    actor_appearances.plot(kind='barh', color='teal')
    plt.title('Top 10 Actors by Number of Appearances', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Appearances', fontsize=14)
    plt.ylabel('Actor', fontsize=14)
    plt.show()


def plot_language_distribution(movies_df):
    # Calculate the number of movies per language
    language_counts = movies_df['original_language'].value_counts()

    # Plot the distribution of movie languages
    plt.figure(figsize=(10, 6))
    plt.pie(language_counts.values, labels=language_counts.index, autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette("hsv", len(language_counts)))
    plt.title('Distribution of Movie Languages', fontsize=16, fontweight='bold')
    plt.show()
