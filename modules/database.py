import sqlite3
from config import settings


def create_connection(db_file=settings.DATABASE_URI):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_movies_table(conn):
    """Create a table in the SQLite database connected by conn"""
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS movies
                     (id INTEGER PRIMARY KEY,
                      title TEXT NOT NULL,
                      release_date TEXT,
                      genre_ids TEXT,
                      popularity Text,
                      vote_average Text,
                      vote_count Text, 
                      original_language Text);''')  # Adjust columns as needed
    except sqlite3.Error as e:
        print(e)


def save_movies_to_db(movies, conn):
    """Save movies data into the movies table in the SQLite database connected by conn"""
    cur = conn.cursor()
    for movie in movies:
        # Assuming 'genre_ids' is a list, convert it to a string for storage
        genre_ids_str = ','.join(str(gid) for gid in movie['genre_ids']) if movie.get('genre_ids') else ''
        cur.execute(
            "INSERT INTO movies (title, release_date, genre_ids, popularity, vote_average, vote_count, original_language) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (movie['title'], movie['release_date'], genre_ids_str, movie['popularity'], movie['vote_average'],
             movie['vote_count'], movie['original_language']))
    conn.commit()


def check_data_exists(conn, table_name='movies'):
    """Check if there is any data in the movies table.

    Args:
        conn: A SQLite database connection object.

    Returns:
        True if data exists in the movies table, False otherwise.
    """
    try:
        cur = conn.cursor()
        # Check if the 'movies' table exists and has data
        cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if cur.fetchone():
            # The table exists, now check if it has any data
            cur.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cur.fetchone()[0]
            return count > 0
        else:
            # The 'movies' table does not exist
            return False
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False


def create_genres_table(conn):
    """Create the genres table in the database."""
    sql_create_genres_table = """
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_genres_table)
    except sqlite3.Error as e:
        print(e)

def save_genres_to_db(genres, conn):
    """Save genre data into the genres table."""
    try:
        c = conn.cursor()
        for genre in genres:
            c.execute("INSERT OR REPLACE INTO genres (id, name) VALUES (?, ?)",
                      (genre['id'], genre['name']))
        conn.commit()
    except sqlite3.Error as e:
        print(e)