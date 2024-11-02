# INSERTING CLEANED BOOKS DATA CSV

from sqlalchemy.orm import sessionmaker
import pandas as pd
import sys
import os

# Add the root directory to the system path for importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from progress_tracker.tracker_app.models import Book, engine  # Use the existing engine

# Step 1: Load the cleaned CSV file into a pandas DataFrame
file_path = "CleanedBooksDataset.csv"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    sys.exit(1)


# Step 2: Remove any remaining null values in case they exist
df.dropna(inplace=True)

# Step 3: Create a session for SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Step 4: Iterate over the DataFrame and insert the data into the books table
for index, row in df.iterrows():
    book = Book(
        title=row['title'],
        authors=row['authors'],
        description=row['description'],
        category=row['category'],
        publish_year=row['publish_year'],  # Assuming the column exists in the books table
        rating=row['rating'],
        pages=row['pages']
    )
    session.add(book)

# Step 5: Commit the session to persist the changes in the database
session.commit()

# Step 6: Close the session
session.close()

print("Books data successfully inserted!")
