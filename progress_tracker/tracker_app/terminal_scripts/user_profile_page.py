import os
import sys
from progress_tracker.db.database import SessionLocal 
from progress_tracker.tracker_app.models import Book, User, Tracker
from progress_tracker.tracker_app.auth import hash_password  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def user_profile(user_id):
    session = SessionLocal()
    try:
        while True:
            print("\nUser Profile:")
            print("1. Change Username")
            print("2. Change Password")
            print("3. Remove Books from Readlist")
            print("4. Go Back to Main Menu")
            choice = input("Choose an option (1-4): ").strip()

            if choice == '1':
                # Change Username
                new_username = input("Enter new username: ").strip()
                if new_username:
                    # Check if the username is already in use by another user
                    existing_user = session.query(User).filter(User.name == new_username).first()
                    if existing_user:
                        print(f"The username '{new_username}' is already taken. Please choose another one.")
                    else:
                        user = session.query(User).filter_by(user_id=user_id).first()
                        if user:
                            user.name = new_username
                            session.commit()
                            print(f"Username updated to {new_username}.")
                        else:
                            print("User not found.")
                else:
                    print("Invalid username.")

            elif choice == '2':
                # Change Password
                new_password = input("Enter new password: ").strip()
                if new_password:
                    user = session.query(User).filter_by(user_id=user_id).first()
                    if user:
                        # Hash the new password before saving it
                        user.password = hash_password(new_password)
                        session.commit()
                        print("Password updated successfully.")
                    else:
                        print("User not found.")
                else:
                    print("Invalid password.")

            elif choice == '3':
                # Remove Books from Readlist
                readlist = session.query(Tracker).filter_by(user_id=user_id).join(Book).all()
                if not readlist:
                    print("No books in your readlist to remove.")
                    continue

                print("\nYour Readlist:")
                for i, entry in enumerate(readlist, 1):
                    print(f"{i}. {entry.book.title} by {entry.book.authors}")

                to_remove = input("Enter the number(s) of the books you'd like to remove (comma-separated): ").strip()
                indices = [int(i.strip()) - 1 for i in to_remove.split(',') if i.strip().isdigit()]

                # Validate and remove books
                for index in indices:
                    if 0 <= index < len(readlist):
                        session.delete(readlist[index])
                        print(f"Removed '{readlist[index].book.title}' from your readlist.")
                    else:
                        print(f"Invalid choice: {index + 1}. Skipping.")

                session.commit()

            elif choice == '4':
                # Go back to main menu
                print("Returning to main menu...")
                break

            else:
                print("Invalid option. Please choose a valid option.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()
