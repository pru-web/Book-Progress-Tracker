# Call this function when the admin wants to manage users

import os
import sys
from sqlalchemy.orm import sessionmaker
from progress_tracker.db.database import SessionLocal
from progress_tracker.tracker_app.models import User
from progress_tracker.tracker_app.auth import hash_password

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def admin_user_management():
    session = SessionLocal()
    try:
        while True:
            print("\nAdmin User Management:")
            print("1. Add User")
            print("2. Remove User")
            print("3. Go Back to Main Menu")
            choice = input("Choose an option (1-3): ").strip()

            if choice == '1':
                # Add User
                username = input("Enter new username: ").strip()
                password = input("Enter new password: ").strip()
                if username and password:
                    hashed_password = hash_password(password)
                    new_user = User(name=username, password=hashed_password)
                    session.add(new_user)
                    session.commit()
                    print(f"User '{username}' added successfully.")
                else:
                    print("Invalid username or password.")

            elif choice == '2':
                # Remove User
                username = input("Enter the username of the user to remove: ").strip()
                user_to_remove = session.query(User).filter_by(name=username).first()
                if user_to_remove:
                    session.delete(user_to_remove)
                    session.commit()
                    print(f"User '{username}' removed successfully.")
                else:
                    print("User not found.")

            elif choice == '3':
                print("Returning to main menu...")
                break

            else:
                print("Invalid option. Please choose a valid option.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


