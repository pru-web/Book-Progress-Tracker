# Entry Point , implementing admin and user interface upon log in

# terminal_scripts/main.py

import sys
import os
from progress_tracker.tracker_app.models import User
from progress_tracker.tracker_app.terminal_scripts.login import login_user
from progress_tracker.tracker_app.terminal_scripts.register import register_user
from progress_tracker.tracker_app.terminal_scripts.menu_page import menu_page
from progress_tracker.tracker_app.terminal_scripts.user_profile_page import user_profile
from progress_tracker.tracker_app.terminal_scripts.progress_tracker_page import progress_tracker_page
from progress_tracker.tracker_app.terminal_scripts.admin_user_management import admin_user_management
from progress_tracker.tracker_app.terminal_scripts.admin_book_management import admin_book_management
from progress_tracker.tracker_app.terminal_scripts.exceptions import InvalidCredentialsException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def admin_menu():
    while True:
        print("\nAdmin Functions:")
        print("1. User Settings")
        print("2. Book Management")
        print("3. Log Out")
        choice = input("Please choose an option (1-4): ")

        if choice == '1':
            admin_user_management()
        elif choice == '2':
            admin_book_management()
        elif choice == '3':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu(user_id):
    while True:
        print("\nUser Functions:")
        print("1. Menu Page")
        print("2. Progress Tracker Page")
        print("3. User Profile")
        print("4. Log Out")

        choice = input("Please choose an option (1-4): ")
        if choice == '1':
            menu_page(user_id)
            
        elif choice == '2':
            progress_tracker_page(user_id)
            
        elif choice == '3':
            user_profile(user_id)
            
        elif choice == '4':
            print("Logging out...")
            return
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    while True:
        print("Welcome to the Progress Tracker!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Please choose an option (1-3): ")

        if choice == '1':
            register_user()
        elif choice == '2':
            try:
                user_id, role = login_user()
                if role == 'admin':
                    admin_menu()  # Show admin menu
                elif role == 'user':
                    user_menu(user_id)  # Show user menu
            except InvalidCredentialsException as e:
                print(e)  # Prints "Invalid username or password."
                print("Login failed, please try again.")
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
