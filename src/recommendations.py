from psycopg import Error
from .validators import validate_int_input


def get_recommendations(connection):
    try:
        print("\nRecommendation Criteria:")
        print("1. Top 5 movies by ratings")
        print("2. Top 5 movies by ratings and genre")
        print("3. Top 5 movies by ratings and release year")
        print("4. Top 5 movies by ratings, genre, and release year")
        print("5. Top 3 movies of a director based on ratings")
        print("6. Top 3 movies of an actor based on ratings")
        print("7. Top 3 movies of a production company based on ratings")

        choice = input("Enter your choice: ")

        base_query = """
            SELECT m.title, AVG(m.rating) AS averagerating
            FROM movies m
        """

        params = None

        if choice == "1":
            query = (
                base_query
                + """
                GROUP BY m.movieid, m.title
                ORDER BY averagerating DESC
                LIMIT 5;
            """
            )
        elif choice == "2":
            genre = input("Enter the genre: ")
            query = (
                base_query
                + """
                WHERE m.genre ILIKE %s
                GROUP BY m.movieid, m.title
                ORDER BY averagerating DESC
                LIMIT 5;
            """
            )
            params = (f"%{genre}%",)
        elif choice == "3":
            release_year = validate_int_input("Enter the release year: ")
            query = (
                base_query
                + """
                WHERE m.releaseyear = %s
                GROUP BY m.movieid, m.title
                ORDER BY averagerating DESC
                LIMIT 5;
            """
            )
            params = (release_year,)
        elif choice == "4":
            genre = input("Enter the genre: ")
            release_year = validate_int_input("Enter the release year: ")
            query = (
                base_query
                + """
                WHERE m.genre ILIKE %s AND m.releaseyear = %s
                GROUP BY m.movieid, m.title
                ORDER BY averagerating DESC
                LIMIT 5;
            """
            )
            params = (f"%{genre}%", release_year)
        elif choice == "5":
            director = input("Enter the director's name: ")
            query = (
                base_query
                + """
                WHERE m.director ILIKE %s
                GROUP BY m.movieid, m.title
                ORDER BY averagerating DESC
                LIMIT 3;
            """
            )
            params = ("%" + director + "%",)
        elif choice == "6":
            actor = input("Enter the actor's name: ")
            query = """
                SELECT m.title, AVG(m.rating) AS averagerating
                FROM movies m
                LEFT JOIN reviews r ON m.movieid = r.movieid
                WHERE m.casting ILIKE %s
                GROUP BY m.movieid, m.title
                ORDER BY averagerating DESC
                LIMIT 3;
            """
            params = ("%" + actor + "%",)
        elif choice == "7":
            company = input("Enter the production company's name: ")
            query = (
                base_query
                + """
                WHERE m.productioncompany ILIKE %s
                GROUP BY m.movieid, m.title
                ORDER BY averagerating DESC
                LIMIT 3;
            """
            )
            params = ("%" + company + "%",)
        else:
            print("\nInvalid choice. Please choose a valid one.")
            get_recommendations(connection)
            return

        with connection.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            recommendations = cursor.fetchall()
            if not recommendations:
                print(
                    "\nThere are no recommended movies with this input. Try a different one."
                )
                get_recommendations(connection)
            else:
                print("\nRecommended movies:")
                for rec in recommendations:
                    print(f"{rec[0]} -- Average Rating: {rec[1]:.1f}")
    except Error as e:
        connection.rollback()
        print(f"Error getting recommendations: {e}")
