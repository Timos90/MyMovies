import psycopg
from psycopg import Error
import environs

# Initialize environs
env = environs.Env()
env.read_env()


def connect_to_db():
    try:
        connection = psycopg.connect(
            user=env.str("DB_USER"),
            password=env("DB_PASSWORD"),
            host=env("DB_HOST"),
            port=env("DB_PORT"),
            dbname=env("DB_NAME"),
        )
        print("Connected to the database.")
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None


def initialize_db(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS movies (
                    movieid SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    releaseyear INTEGER NOT NULL,
                    genre VARCHAR(255),
                    director VARCHAR(255),
                    rating DOUBLE PRECISION,
                    runtime INTEGER,
                    description TEXT,
                    language VARCHAR(255),
                    country VARCHAR(255),
                    boxoffice BIGINT,
                    awards TEXT,
                    casting TEXT,
                    productioncompany VARCHAR(255),
                    budget BIGINT,
                    releasedate DATE,
                    productioncompanyid INT,
                    deleted BOOLEAN DEFAULT false,
                    added_by_user_id INT,
                    FOREIGN KEY (added_by_user_id) REFERENCES users(user_id)
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_movies (
                    user_movie_id serial PRIMARY KEY,
                    user_id integer NOT NULL,
                    movieid integer NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (movieid) REFERENCES movies(movieid) ON DELETE CASCADE
                );

            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id SERIAL PRIMARY KEY,
                    user_id INTEGER,
                    movieid INTEGER,
                    review TEXT,
                    review_date DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (movieid) REFERENCES movies(movieid) ON DELETE CASCADE
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ratings (
                    rating_id serial PRIMARY KEY,
                    user_id INTEGER,
                    movieid INTEGER,
                    rating DOUBLE PRECISION,
                    rating_date DATE DEFAULT CURRENT_DATE,
                    CONSTRAINT ratings_rating_check CHECK (rating >= 1.0 AND rating <= 10.0),
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (movieid) REFERENCES movies(movieid) ON DELETE CASCADE
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS watchlist (
                    watchlist_id SERIAL PRIMARY KEY,
                    user_id INTEGER,
                    movieid INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (movieid) REFERENCES movies(movieid) ON DELETE CASCADE
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS deleted_movies (
                user_id INT,
                movieid INT,
                PRIMARY KEY (user_id, movieid),
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (movieid) REFERENCES movies(movieid)
                );
            """
            )
            connection.commit()
    except Error as e:
        connection.rollback()
        print(f"Error initializing database: {e}")
