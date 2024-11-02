import os
import sys
from sqlalchemy.orm import sessionmaker
from progress_tracker.db.database import SessionLocal 
from progress_tracker.tracker_app.models import Book,Tracker


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


def progress_tracker_page(user_id):
    from progress_tracker.tracker_app.terminal_scripts.main_menu import user_menu
    session = SessionLocal()
    try:
        while True:
            # Fetch user-specific readlist
            readlist = session.query(Tracker).filter_by(user_id=user_id).join(Book).all()
            if not readlist:
                print("Your readlist is empty. Add books from the Menu Page.")
                break

            print("\nYour Readlist:")
            for i, entry in enumerate(readlist, 1):
                book = entry.book
                print(f"{i}. {book.title} by {book.authors}")
                print(f"   Status: {entry.status}")
                print(f"   Progress: {entry.progress} pages out of {book.pages if book.pages else 'Unknown'}\n")

            print("\nOptions:")
            print("1. Update Book Status")
            print("2. Rate Completed Book")
            print("3. Go Back to Main Menu")
            choice = input("Choose an option (1-3): ")

            if choice == '1':
                update_book_status(user_id)
                # Refresh the readlist entries for updated values
                for entry in readlist:
                    session.refresh(entry)  # Ensures each entry is refreshed with the latest data
                continue 

            elif choice == '2':
                rate_completed_book(user_id)
                # Refresh the readlist entries for updated values
                for entry in readlist:
                    session.refresh(entry)  # Ensures each entry is refreshed with the latest data

            elif choice == '3':
                user_menu(user_id)
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        session.close()

def update_book_status(user_id):
    session = SessionLocal()
    try:
        # Show books in readlist for status update
        readlist = session.query(Tracker).filter_by(user_id=user_id).join(Book).all()
        if not readlist:
            print("No books in your readlist.")
            return

        for i, entry in enumerate(readlist, 1):
            print(f"{i}. {entry.book.title} - Current Status: {entry.status}")

        choice = input("Enter the number of the book you'd like to update: ")
        try:
            selected_entry = readlist[int(choice) - 1]
        except (IndexError, ValueError):
            print("Invalid choice.")
            return

        # Update the status
        print("Status options: 1. Not Yet Completed/Started, 2. In Progress, 3. Complete")
        status_choice = input("Choose a status option (1-3): ")
        if status_choice == '1':
            selected_entry.status = 'Not Yet Completed/Started'
            selected_entry.progress = 0
        elif status_choice == '2':
            selected_entry.status = 'In Progress'
            try:
                current_page = int(input("Enter the page number you're on: "))
                if  selected_entry.book.pages and current_page >= selected_entry.book.pages:
                    selected_entry.status = 'Complete'
                    selected_entry.progress = selected_entry.book.pages
                    print(f"{selected_entry.book.title} marked as Complete at page {selected_entry.book.pages}.")
                else:
                    selected_entry.progress = current_page
                    print(f"{selected_entry.book.title} marked as In Progress at page {current_page}.")
            except ValueError:
                print("Invalid page number.")
                return
        elif status_choice == '3':
            selected_entry.status = 'Complete'
            selected_entry.progress = selected_entry.book.pages or 0
            print(f"{selected_entry.book.title} marked as Complete with progress set to {selected_entry.book.pages} pages.")
        else:
            print("Invalid status option.")

        session.commit()
    finally:
        session.close()

def rate_completed_book(user_id):
    session = SessionLocal()
    try:
        # Display completed books for rating
        completed_books = session.query(Tracker).filter_by(user_id=user_id, status='Complete').join(Book).all()
        if not completed_books:
            print("No completed books available to rate.")
            return

        for i, entry in enumerate(completed_books, 1):
            print(f"{i}. {entry.book.title}")

        choice = input("Enter the number of the book you'd like to rate: ")
        try:
            selected_entry = completed_books[int(choice) - 1]
        except (IndexError, ValueError):
            print("Invalid choice.")
            return

        # Prompt for rating input
        try:
            rating = float(input("Enter your rating (1-5): ").strip())
            if 1 <= rating <= 5:
                selected_entry.book.rating = rating
                session.commit()
                print(f"Rated '{selected_entry.book.title}' with {rating} stars.")
            else:
                print("Rating must be between 1 and 5.")
        except ValueError:
            print("Invalid rating input.")
    finally:
        session.close()