import re
import getpass
from psycopg import Error


def register_user(connection):
    try:
        with connection.cursor() as cursor:
            while True:
                username = input("Enter a username (at least 5 characters): ").strip()
                if len(username) < 5:
                    print("Username must be at least 5 characters long.")
                else:
                    break

            while True:
                password = input(
                    "Enter a password (at least 8 characters, "
                    "1 uppercase, 1 digit, 1 special character): "
                ).strip()

                if len(password) < 8:
                    print("Password must be at least 8 characters long.")
                elif not re.search(r"[A-Z]", password):
                    print("Password must contain at least one uppercase letter.")
                elif not re.search(r"\d", password):
                    print("Password must contain at least one digit.")
                elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                    print("Password must contain at least one special character.")
                else:
                    break

            # Execute SQL insertion
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id;",
                (username, password),
            )
            user_id = cursor.fetchone()[0]
            connection.commit()
            print("\nUser registered successfully.")
            return user_id

    except Error as e:
        connection.rollback()
        print(f"Error registering user: {e}")


def login_user(connection):
    try:
        with connection.cursor() as cursor:
            # Get username and validate
            while True:
                username = input("Enter your username: ").strip()
                if len(username) < 5:
                    print("Username must be at least 5 characters long.")
                else:
                    break

            # Get password and validate
            while True:
                password = getpass.getpass(
                    "Enter your password (at least 8 characters, "
                    "1 uppercase, 1 digit, 1 special character): "
                )

                if len(password) < 8:
                    print("Password must be at least 8 characters long.")
                elif not re.search(r"[A-Z]", password):
                    print("Password must contain at least one uppercase letter.")
                elif not re.search(r"\d", password):
                    print("Password must contain at least one digit.")
                elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                    print("Password must contain at least one special character.")
                else:
                    break

            cursor.execute(
                "SELECT user_id FROM users WHERE username = %s AND password = %s;",
                (username, password),
            )
            user = cursor.fetchone()

            if user:
                print("Login successful.")
                return user[0]
            else:
                print("Invalid username or password.")
                return None
    except Error as e:
        print(f"Error during login: {e}")
        return None
