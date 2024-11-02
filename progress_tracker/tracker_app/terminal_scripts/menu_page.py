# Welcome Page -> User log_in -> user_menu -> .

import os
import sys
from sqlalchemy.orm import sessionmaker
from progress_tracker.db.database import SessionLocal 
from progress_tracker.tracker_app.models import Book , Tracker
from progress_tracker.tracker_app.terminal_scripts.exceptions import BookNotFoundException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def view_books():
    # logic to fetch and display book data from the database
    session = SessionLocal()
    try:
        books = session.query(Book).limit(100).all() # There are 62558 book records in dataset displaying only 100 for now
        print("\nAvailable Books:")
        for book in books:
                print(f"""
                Title: {book.title}
                Author: {book.authors}
                Description: {book.description}
                Category: {book.category}
                Publish Year: {book.publish_year}
                Rating: {book.rating}
                Pages: {book.pages}
                """)
    except Exception as e:
        print(f"An error occurred while fetching books: {e}")
    finally:
        session.close()

def search_books(user_id):
    """Allows user to search for a book by title and ADD BOOK TO READLIST FROM HERE."""
    session = SessionLocal()
    try:
        title = input("Enter the title of the book you want to search for: ").strip().lower()
        results = session.query(Book).filter(
            (Book.title.ilike(f"%{title}%")) | 
            (Book.authors.ilike(f"%{title}%"))
        ).all()

        if not results:
            raise BookNotFoundException()

        print("\nSearch Results:")
        for i, book in enumerate(results, 1):
            print(f"""
            {i}.Title: {book.title}
            Author: {book.authors}
            Description: {book.description}
            Category: {book.category}
            Publish Year: {book.publish_year}
            Rating: {book.rating}
            Pages: {book.pages}
            """)
        # Prompt user to select a book to add to their readlist
        choice = input("Enter the number of the book to add it to your readlist, or press Enter to skip: ").strip()
        if choice:
            try:
                chosen_book = results[int(choice) - 1]
            except (IndexError, ValueError):
                print("Invalid choice. Please try again.")
                return
            
            # Check if the book is already in the user's readlist
            exists = session.query(Tracker).filter_by(user_id=user_id, book_id=chosen_book.book_id).first()
            if exists:
                print("This book is already in your readlist.")
            else:
                # Add the selected book to the user's readlist with an initial status
                new_entry = Tracker(user_id=user_id, book_id=chosen_book.book_id, status='Not Yet Completed/Started', progress=0)
                session.add(new_entry)
                session.commit()
                print(f"Book '{chosen_book.title}' added to your readlist.")

    except BookNotFoundException as e:
        print(e)
    except Exception as e:
        print(f"An error occurred during the search: {e}")
    finally:
        session.close()

def menu_page(user_id):
    while True:
        print("\n--- Menu Page ---")
        print("1. View Books")
        print("2. Search Books & Add To Readlist")
        print("3. Return to Main Menu")
        
        choice = input("Please choose an option (1-3): ")
        
        if choice == '1':
            view_books()
        elif choice == '2':
            search_books(user_id)
        elif choice == '3':
            break  # Return to the main user menu
        else:
            print("Invalid choice. Please try again.")