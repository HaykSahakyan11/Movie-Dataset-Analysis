from modules.api import fetch_popular_movies, fetch_movie_genres
from modules.database import create_connection, save_movies_to_db, create_movies_table, check_data_exists, \
    create_genres_table, save_genres_to_db
from modules.analysis import load_movies_from_db, load_genres_from_db, plot_genre_distribution, \
    plot_release_year_distribution, plot_average_popularity_by_genre, plot_average_vote_count_by_genre, \
    plot_movies_over_time, plot_language_distribution


def main():
    conn = create_connection()
    create_movies_table(conn)  # Ensure the movies table is created
    create_genres_table(conn)  # Ensure the genres table is created

    # Check if data exists in the database
    if not check_data_exists(conn):
        # Data does not exist, fetch from API and save to DB
        movies = fetch_popular_movies()
        save_movies_to_db(movies, conn)
    else:
        print("Using existing data in the database.")

    # Check and fetch genres if genres table is empty
    if not check_data_exists(conn, table_name='genres'):
        genres = fetch_movie_genres()
        save_genres_to_db(genres, conn)

    # Load movies for analysis from the database
    movies_df = load_movies_from_db(conn)
    genres_df = load_genres_from_db(conn)

    # Perform data analysis and visualization
    perform_data_analysis(movies_df, genres_df)


def perform_data_analysis(movies_df, genres_df):
    """Perform data analysis and visualization on the given dataframes."""
    plot_genre_distribution(movies_df, genres_df)
    plot_release_year_distribution(movies_df)
    plot_average_popularity_by_genre(movies_df, genres_df)
    plot_average_vote_count_by_genre(movies_df, genres_df)
    plot_movies_over_time(movies_df)
    plot_language_distribution(movies_df)


if __name__ == '__main__':
    main()
