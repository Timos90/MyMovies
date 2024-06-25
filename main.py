from src.db import connect_to_db, initialize_db
from src.user import register_user, login_user
from src.menu import menu
import time


def main():
    connection = connect_to_db()
    if connection:
        initialize_db(connection)

        print("\nWelcome to the Movie Database Application!")
        while True:
            print("\n1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("\nEnter your choice: ")

            if choice == "1":
                register_user(connection)
            elif choice == "2":
                user_id = login_user(connection)
                if user_id:
                    menu(connection, user_id)
            elif choice == "3":
                print("\nExiting...")
                time.sleep(2)
                print("Thank you for using The Movie Application!!!")
                break
            else:
                print("Invalid choice. Please try again.")
                print("-" * 20)

        connection.close()


if __name__ == "__main__":
    main()
