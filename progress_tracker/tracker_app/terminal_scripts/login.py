#Users will input their username and password, which will be verified against the database
#checking according to credential match if user logging is an admin

from progress_tracker.db.database import SessionLocal
from progress_tracker.tracker_app.models import User, Admin
from progress_tracker.tracker_app.auth import check_password
from progress_tracker.tracker_app.terminal_scripts.exceptions import InvalidCredentialsException

# login.py

def login_user():
    session = SessionLocal()
    try:
        name = input("Enter your username: ")
        password = input("Enter your password: ")

        user = session.query(User).filter_by(name=name).first()
        if user and check_password(user.password, password):
            print(f"Login successful! Welcome, {user.name}. You are logged in as a regular user.")
            return user.user_id, 'user'  # Return the user role for regular users nad user id to main menu
        
        admin = session.query(Admin).filter_by(name=name).first()
        if admin and check_password(admin.password, password):
            print(f"Login successful! Welcome, {admin.name}. You are logged in as an admin.")
            return None,'admin'  # Return the role for admins
            
        raise InvalidCredentialsException()
        #return None,None

    finally:
        session.close()
