
# Call this function when the admin wants to edit books
import os
import sys
from sqlalchemy.orm import sessionmaker
from progress_tracker.db.database import SessionLocal
from progress_tracker.tracker_app.models import Book
from progress_tracker.tracker_app.terminal_scripts.exceptions import BookNotFoundException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def admin_book_management():
    session = SessionLocal()
    try:
        while True:
            print("\nAdmin Book Editing:")
            print("1. Edit Book Details")
            print("2. Remove Book")
            print("3. Go Back to Main Menu")
            choice = input("Choose an option (1-3): ").strip()

            if choice == '1':
                # Edit Book Details
                book_id = input("Enter the ID of the book to edit: ").strip()
                book = session.query(Book).filter_by(book_id=book_id).first()
                if not book:
                    raise BookNotFoundException()
                if book:
                    print(f"Current details for '{book.title}':")
                    print(f"Authors: {book.authors}")
                    print(f"Description: {book.description}")
                    print(f"Pages: {book.pages}")
                    print(f"Rating: {book.rating}")

                    # Update parameters
                    book.title = input("Enter new title (leave blank to keep current): ") or book.title
                    book.authors = input("Enter new authors (leave blank to keep current): ") or book.authors
                    book.description = input("Enter new description (leave blank to keep current): ") or book.description
                    pages_input = input("Enter new pages (leave blank to keep current): ")
                    book.pages = int(pages_input) if pages_input else book.pages
                    rating_input = input("Enter new rating (leave blank to keep current): ")
                    book.rating = float(rating_input) if rating_input else book.rating

                    session.commit()
                    print(f"Book '{book.title}' updated successfully.")


            elif choice == '2':
                # Remove Book
                book_id = input("Enter the ID of the book to remove: ").strip()
                book_to_remove = session.query(Book).filter_by(book_id=book_id).first()
                if not book_to_remove:
                    raise BookNotFoundException()
                
                session.delete(book_to_remove)
                session.commit()
                print(f"Book '{book_to_remove.title}' removed successfully.")

            elif choice == '3':
                print("Returning to main menu...")
                break

            else:
                print("Invalid option. Please choose a valid option.")
                
    except BookNotFoundException as e:
        print(e)  # Display the custom exception message
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


