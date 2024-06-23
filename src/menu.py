from psycopg2 import Error
from .validators import validate_int_input, validate_float_input, validate_date_input
from .recommendations import get_recommendations

def display_menu():
    print("\nMovie Database Menu:")
    print("1. View all movies")
    print("2. View details of a movie")
    print("3. Add a new movie")
    print("4. View my movies")
    print("5. Delete a movie from my collection")
    print("6. Rate a movie")
    print("7. Add review to a movie")
    print("8. Get movie recommendations")
    print("9. View my reviews")
    print("10. Add a movie to my watchlist")
    print("11. View my watchlist")
    print("12. Exit")

def view_movies(connection, user_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT movieid, title, releaseyear 
                FROM movies 
                WHERE movieid NOT IN (SELECT movieid FROM deleted_movies WHERE user_id = %s)
                ORDER BY movieid;
            """, (user_id,))
            movies = cursor.fetchall()
            print("\nAll Movies:")
            for movie in movies:
                print(f"{movie[0]}: {movie[1]} ({movie[2]})")
    except Error as e:
        print(f"Error retrieving movies: {e}")


def view_movie_details(connection):
    movie_id = validate_int_input("Enter the MovieID of the movie: ")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM movies WHERE movieid = %s;", (movie_id,))
            movie = cursor.fetchone()
            if movie:
                print(f"\nDetails of MovieID {movie_id}:")
                print(f"Title: {movie[1]}")
                print(f"Release Year: {movie[2]}")
                print(f"Genre: {movie[3]}")
                print(f"Director: {movie[4]}")
                print(f"Rating: {movie[5]}")
                print(f"Runtime: {movie[6]} minutes")
                print(f"Description: {movie[7]}")
                print(f"Language: {movie[8]}")
                print(f"Country: {movie[9]}")
                print(f"Box Office: ${movie[10]:,}")
                print(f"Awards: {movie[11]}")
                print(f"Casting: {movie[12]}")
                print(f"Production Company: {movie[13]}")
                print(f"Budget: ${movie[14]:,}")
                print(f"Release Date: {movie[15]}")
            else:
                print("Movie not found.")
    except Error as e:
        print(f"Error retrieving movie details: {e}")

def add_movie(connection, user_id):
    try:
        title = input("Enter the title of the movie: ")
        release_year = validate_int_input("Enter the release year of the movie: ")
        genre = input("Enter the genre of the movie: ")
        director = input("Enter the director of the movie: ")
        rating = validate_float_input("Enter the rating of the movie: ", min_value=1.0, max_value=10.0)
        runtime = validate_int_input("Enter the runtime (in minutes) of the movie: ")
        description = input("Enter the description of the movie: ")
        language = input("Enter the language of the movie: ")
        country = input("Enter the country of origin of the movie: ")
        box_office = validate_int_input("Enter the box office earnings of the movie: ")
        awards = input("Enter the awards won by the movie: ")
        casting = input("Enter the cast of the movie: ")
        production_company = input("Enter the production company of the movie: ")
        budget = validate_int_input("Enter the budget of the movie: ")
        release_date = validate_date_input("Enter the release date of the movie (YYYY-MM-DD): ")

        with connection.cursor() as cursor:
            # Find the first available MovieID
            cursor.execute("""
                SELECT MIN(m1.movieid + 1)
                FROM movies m1
                LEFT JOIN movies m2 ON m1.movieid + 1 = m2.movieid
                WHERE m2.movieid IS NULL;
            """)
            available_id = cursor.fetchone()[0]

            if available_id is None:
                # If there are no gaps, find the max ID and add 1
                cursor.execute("SELECT COALESCE(MAX(movieid), 0) + 1 FROM movies;")
                available_id = cursor.fetchone()[0]

            # Insert the new movie with the available ID
            cursor.execute("""
                INSERT INTO movies (MovieID, Title, ReleaseYear, Genre, Director, Rating,
                                    Runtime, Description, Language, Country, BoxOffice, Awards,
                                    Casting, ProductionCompany, Budget, ReleaseDate, added_by_user_id
                                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (available_id, title, release_year, genre, director, rating,
                  runtime, description, language, country, box_office, awards,
                  casting, production_company, budget, release_date, user_id
                 ))

            # Add the movie to the user's collection
            cursor.execute("INSERT INTO user_movies (user_id, movieid) VALUES (%s, %s);",
                           (user_id, available_id))

            connection.commit()
            print("Movie added successfully with MovieID:", available_id)
    except Error as e:
        connection.rollback()
        print(f"Error adding movie: {e}")


def view_user_movies(connection, user_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT m.movieid, m.title, m.releaseyear 
                FROM movies m
                JOIN user_movies um ON m.movieid = um.movieid
                WHERE um.user_id = %s
                ORDER BY m.movieid;
            """, (user_id,))
            movies = cursor.fetchall()
            if movies:
                print("\nYour Movies:")
                for movie in movies:
                    print(f"{movie[0]}: {movie[1]} ({movie[2]})")
            else:
                print("You haven't added any movies yet")
    except Error as e:
        print(f"Error retrieving your movies: {e}")


def delete_movie(connection, user_id):
    movie_id = validate_int_input("Enter the MovieID of the movie to delete: ")
    try:
        with connection.cursor() as cursor:
            # Check if the user is the one who added the movie
            cursor.execute("SELECT added_by_user_id FROM movies WHERE movieid = %s;", (movie_id,))
            added_by_user_id = cursor.fetchone()
            if added_by_user_id and added_by_user_id[0] == user_id:
                # If the user added the movie, delete it for everyone
                cursor.execute("DELETE FROM movies WHERE movieid = %s;", (movie_id,))
                cursor.execute("DELETE FROM user_movies WHERE movieid = %s;", (movie_id,))
                cursor.execute("DELETE FROM deleted_movies WHERE movieid = %s;", (movie_id,))
                connection.commit()
                print("Movie deleted successfully for everyone.")
            else:
                # If the user did not add the movie, add it to the deleted_movies table
                cursor.execute("INSERT INTO deleted_movies (user_id, movieid) VALUES (%s, %s);",
                               (user_id, movie_id))
                connection.commit()
                print("Movie deleted successfully from your collection and will not be visible in your list.")
    except Error as e:
        connection.rollback()
        print(f"Error deleting movie: {e}")


def rate_movie(connection, user_id):
    movie_id = validate_int_input("Enter the MovieID of the movie to rate: ")
    rating = validate_float_input("Enter your rating (1.0 to 10.0): ", min_value=1.0, max_value=10.0)
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ratings (user_id, movieid, rating) VALUES (%s, %s, %s);",
                           (user_id, movie_id, rating)
                          )
            connection.commit()
            print("Movie rated successfully.")

            cursor.execute("""
                SELECT r.rating, u.username, r.rating_date 
                FROM ratings r 
                JOIN users u ON r.user_id = u.user_id 
                WHERE r.movieid = %s 
                ORDER BY r.rating_date DESC;
            """, (movie_id,))
            ratings = cursor.fetchall()

            if ratings:
                print("\nCurrent Ratings for the movie:")
                for rat in ratings:
                    print(f"\nRating: {rat[0]:.1f}")
                    print(f"User: {rat[1]}")
                    print(f"Date: {rat[2]}")
                    print("-" * 20)
            else:
                print("No ratings available for this movie yet.")
    except Error as e:
        connection.rollback()
        print(f"Error rating movie: {e}")

def add_review(connection, user_id):
    movie_id = validate_int_input("Enter the MovieID of the movie to review: ")
    review_text = input("Enter your review: ")
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO reviews (user_id, movieid, review) VALUES (%s, %s, %s);",
                           (user_id, movie_id, review_text)
                          )
            connection.commit()
            print("Review added successfully.")
    except Error as e:
        connection.rollback()
        print(f"Error adding review: {e}")

def view_user_reviews(connection, user_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT m.title, r.review, r.review_date
                FROM reviews r
                JOIN movies m ON r.movieid = m.movieid
                WHERE r.user_id = %s
                ORDER BY r.review_date DESC;
            """, (user_id,))
            reviews = cursor.fetchall()

            if reviews:
                print("\nYour Reviews:")
                for review in reviews:
                    print(f"\nMovie: {review[0]}")
                    print(f"Review: {review[1]}")
                    print(f"Date: {review[2]}")
                    print("-" * 20)
            else:
                print("You haven't reviewed any movies yet.")
    except Error as e:
        print(f"Error retrieving your reviews: {e}")

def add_to_watchlist(connection, user_id):
    movie_id = validate_int_input("Enter the MovieID to add to your watchlist: ")

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO watchlist (user_id, movieid)
                VALUES (%s, %s);
            """, (user_id, movie_id))
            connection.commit()
            print("Movie added to your watchlist successfully.")
    except Error as e:
        connection.rollback()
        print(f"Error adding movie to watchlist: {e}")

def view_watchlist(connection, user_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT w.watchlist_id, m.movieid, m.title, m.releaseyear
                FROM watchlist w
                JOIN movies m ON w.movieid = m.movieid
                WHERE w.user_id = %s
                ORDER BY w.watchlist_id;
            """, (user_id,))
            watchlist_items = cursor.fetchall()

            if not watchlist_items:
                print("Your watchlist is empty.")
            else:
                print("\nYour Watchlist:")
                for item in watchlist_items:
                    print(f"{item[0]} - {item[2]} ({item[3]})")

    except Error as e:
        print(f"Error viewing watchlist: {e}")

def menu(connection, user_id):
    while True:
        display_menu()
        choice = input("\nEnter your choice: ")

        if choice == '1':
            print("*"*30)
            view_movies(connection, user_id)
            print("*"*30)
        elif choice == '2':
            print("*"*30)
            view_movie_details(connection)
            print("*"*30)
        elif choice == '3':
            print("*"*30)
            add_movie(connection,user_id)
            print("*"*30)
        elif choice == '4':
            print("*"*30)
            view_user_movies(connection, user_id)
            print("*"*30)
        elif choice == '5':
            print("*"*30)
            delete_movie(connection, user_id)
            print("*"*30)
        elif choice == '6':
            print("*"*30)
            rate_movie(connection, user_id)
            print("*"*30)
        elif choice == '7':
            print("*"*30)
            add_review(connection, user_id)
            print("*"*30)
        elif choice == '8':
            print("*"*30)
            get_recommendations(connection)
            print("*"*30)
        elif choice == '9':
            print("*"*30)
            view_user_reviews(connection, user_id)
            print("*"*30)
        elif choice == '10':
            print("*"*30)
            add_to_watchlist(connection, user_id)
            print("*"*30)
        elif choice == '11':
            print("*"*30)
            view_watchlist(connection, user_id)
            print("*"*30)
        elif choice == '12':
            print("*"*15)
            print("\nGoodbye User!!!")
            print("*"*15)
            break
        else:
            print("Invalid choice. Please try again.")
