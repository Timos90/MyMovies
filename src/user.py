from psycopg2 import Error
import getpass

def register_user(connection):
    try:
        with connection.cursor() as cursor:
            username = input("Enter a username: ")
            password = getpass.getpass("Enter a password: ")

            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id;",
                            (username, password))
            user_id = cursor.fetchone()[0]
            connection.commit()
            print("User registered successfully.")
            return user_id
    except Error as e:
        connection.rollback()
        print(f"Error registering user: {e}")

def login_user(connection):
    try:
        with connection.cursor() as cursor:
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")

            cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s;",
                            (username, password))
            user = cursor.fetchone()

            if user:
                print("Login successful.")
                return user[0]
            else:
                print("Invalid username or password.")
                print("*"*30)
                return None
    except Error as e:
        print(f"Error during login: {e}")
        return None
