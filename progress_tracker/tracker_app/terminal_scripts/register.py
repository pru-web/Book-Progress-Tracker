# registers a new user by taking their username and password input. Password hashing is applied before saving the password to the database

from progress_tracker.db.database import SessionLocal
from progress_tracker.tracker_app.models import User
from progress_tracker.tracker_app.auth import hash_password

def register_user():
    session = SessionLocal()
    try:
        name = input("Enter your desired username: ")
        password = input("Enter your desired password: ")
        password_confirm = input("Confirm your password: ")

        if password != password_confirm:
            print("Passwords do not match. Please try again.")
            return False
        
        # Hash the password before storing it in the database
        hashed_password = hash_password(password)

        new_user = User(name=name, password=hashed_password)
        session.add(new_user)
        session.commit()
        print(f"User {name} registered successfully.")
        return True
    finally:
        session.close()

if __name__ == "__main__":
    register_user()
