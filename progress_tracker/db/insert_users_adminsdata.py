# insert_users_admin.py
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from progress_tracker.tracker_app.auth import hash_password
from progress_tracker.tracker_app.models import User,Admin, engine

# Step 1: Create a session for SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Step 2: Insert data into the users table
users_data = [
    {'name': 'John Doe', 'password': 'password123'},
    {'name': 'Jane Smith', 'password': 'securepass'},
    {'name': 'Alice Brown', 'password': 'alice123'},
    {'name': 'Bob White', 'password': 'bobstrong'}
]

for user in users_data:
    new_user = User(
        name=user['name'],
        password=hash_password(user['password'])
    )
    session.add(new_user)

# Step 3: Insert data into the admin table
admin_data = [
    {'name': 'admin1', 'password': 'adminpassword1'}
]

for admin in admin_data:
    new_admin = Admin(
        name=admin['name'],
        password=hash_password(admin['password'])
    )
    session.add(new_admin)

# Step 4: Commit the session to persist the changes in the database
session.commit()

# Step 5: Close the session
session.close()

print("Users and admin data successfully inserted!")
