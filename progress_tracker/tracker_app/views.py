#Handles the logic to render different views/pages (login, tracker, etc.).

from django.shortcuts import render, redirect
from progress_tracker.tracker_app.models import User, Admin , Book, Tracker # SQLAlchemy models
from progress_tracker.db.database import SessionLocal
from progress_tracker.tracker_app.auth import check_password,hash_password # Function to verify passwords
from progress_tracker.tracker_app.terminal_scripts.exceptions import InvalidCredentialsException, BookNotFoundException
from django.contrib import messages
from sqlalchemy.orm import joinedload


def login_view(request):
    """
    Handles the login functionality. Authenticates using SQLAlchemy models and sets cookies for session tracking.
    """
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')

        session = SessionLocal()  # Start a new SQLAlchemy session
        try:
            # Check if user exists and password matches
            user = session.query(User).filter_by(name=name).first()
            if user and check_password(user.password, password):
                response = redirect('user_main')  # Redirect to user dashboard
                response.set_cookie('user_id', user.user_id, max_age=86400)  # 1-day expiration
                response.set_cookie('role', 'user', max_age=86400)
                return response

            # Check if admin exists and password matches
            admin = session.query(Admin).filter_by(name=name).first()
            if admin and check_password(admin.password, password):
                response = redirect('admin_main')  # Redirect to admin dashboard
                response.set_cookie('admin_id', admin.admin_id, max_age=86400)
                response.set_cookie('role', 'admin', max_age=86400)
                return response

            # Raise an exception if credentials are invalid
            raise InvalidCredentialsException()

        except InvalidCredentialsException as e:
            return render(request, 'tracker_app/login.html', {'error': 'Invalid username or password.'})
        
        finally:
            session.close()  # Close the SQLAlchemy session

    return render(request, 'tracker_app/login.html')


def user_main(request):
    """
    User main page that checks for user authentication via cookies.
    """
    user_id = request.COOKIES.get('user_id')
    role = request.COOKIES.get('role')

    if user_id and role == 'user':
        session = SessionLocal()  # Create a new SQLAlchemy session
        try:
            # Query the User table to get the user object
            user = session.query(User).filter_by(user_id=user_id).first()
            print(user)
            if user:
                    return render(request, 'tracker_app/user_main.html', {'user': user,'user_id': user_id})  # Pass user to template
            else:
                return redirect('login')  # Redirect if user is not found
        finally:
            session.close()  # Ensure the session is closed after the operation
    else:
        return redirect('tracker_app/home.html')  # Redirect to login if no valid user cookie is found


def admin_main(request):
    """
    Admin main page that checks for admin authentication via cookies.
    """
    admin_id = request.COOKIES.get('admin_id')
    role = request.COOKIES.get('role')
    if admin_id and role == 'admin':
        return render(request, 'tracker_app/admin_main.html')
    else:
        return redirect('home')


def logout_view(request):
    """
    Clears the cookies to log the user out and redirects to the login page.
    """
    response = redirect('home')
    response.delete_cookie('user_id')
    response.delete_cookie('admin_id')
    response.delete_cookie('role')
    return response


def register_view(request):
    """
    Registration view for new users.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        # Hash the password before storing it
        hashed_password = hash_password(password)  # Implement this in your auth module

        session = SessionLocal()
        try:
            # Check if the username is already taken
            existing_user = session.query(User).filter_by(name=name).first()
            if existing_user:
                return render(request, 'tracker_app/register.html', {'error': 'Username already exists'})

            # Create a new user
            new_user = User(name=name, password=hashed_password)
            session.add(new_user)
            session.commit()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('home')  # Redirect to the named URL pattern for home

        finally:
            session.close()

    return render(request, 'tracker_app/register.html')

def home_view(request):
    """
    Renders the home page.
    """
    return render(request, 'tracker_app/home.html')

#MENU PAGE (VIEW BOOK AND SEARCH BOOK AND ADD TO READLIST) 

def user_menu(request, user_id = None):
    context = {'user_id': user_id} if user_id else {}
    return render(request, 'tracker_app/user_menu.html', {'user_id': user_id})

def view_books(request):
    session = SessionLocal()
    books = []
    user_id = request.GET.get('user_id')
    try:
        # Limit to 100 books for display purposes
        books = session.query(Book).limit(200).all()
    except Exception as e:
        print(f"An error occurred while fetching books: {e}")
    finally:
        session.close()

    return render(request, 'tracker_app/view_books.html', {'books': books, 'user_id': user_id})

def search_books(request, user_id):
    session = SessionLocal()
    results = []
    message = ""
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip().lower()
        try:
            # Search for books by title or author
            results = session.query(Book).filter(
                (Book.title.ilike(f"%{title}%")) | 
                (Book.authors.ilike(f"%{title}%"))
            ).all()
            if not results:
                raise BookNotFoundException("No books found with that title or author.")
        except BookNotFoundException as e:
            return render(request, 'tracker_app/search_books.html', {'error': e.message, 'user_id': user_id})
        except Exception as e:
            print(f"An error occurred during the search: {e}")
        finally:
            session.close()
    
    # Handle "Add to Readlist" if a book_id is provided
    elif 'book_id' in request.GET:
        book_id = int(request.GET.get('book_id'))
        try:
            # Re-open session to perform add-to-readlist operation
            session = SessionLocal()
            # Check if the book is already in the user's readlist
            exists = session.query(Tracker).filter_by(user_id=user_id, book_id=book_id).first()
            if not exists:
                new_entry = Tracker(user_id=user_id, book_id=book_id, status='Not Yet Completed/Started', progress=0)
                session.add(new_entry)
                session.commit()
                message = "Book added to your readlist."
            else:
                message = "This book is already in your readlist."
        except Exception as e:
            print(f"An error occurred while adding the book to readlist: {e}")
        finally:
            session.close()

    return render(request, 'tracker_app/search_books.html', {'results': results, 'user_id': user_id, 'message': message})

#PROGRESS_TRACKER PAGE (INPUT PROGRESS, VIEW READLIST, RATE BOOKS)

def progress_tracker_page_view(request, user_id):
    session = SessionLocal()
    try:
        # Get the user's readlist
        readlist = session.query(Tracker).filter_by(user_id=user_id).join(Book).all()

        if request.method == "POST":
            # Update status or rating based on form inputs
            action = request.POST.get("action")
            tracker_id = request.POST.get("tracker_id")
            new_status = request.POST.get("status")
            progress_page = request.POST.get("progress_page", None)
            
            selected_entry = session.query(Tracker).get(tracker_id)

            if not selected_entry:
                # Handle the case when the selected tracker entry does not exist
                messages.error(request, "The selected book entry was not found.")
                return redirect("progress_tracker_page", user_id=user_id)
            
            if action == "update_status":
                #new_status = request.POST.get("status")
                selected_entry.status = new_status

                if new_status == "Complete":
                    selected_entry.progress = selected_entry.book.pages or 0
                elif new_status == "In Progress":
                    progress_page = int(request.POST.get("progress_page", 0))

                     # Validate progress page count
                    if progress_page > (selected_entry.book.pages or 0):
                        messages.error(request, "Progress cannot exceed the total number of pages in the book.")
                    else:
                        selected_entry.progress = progress_page
                        messages.success(request, "Book progress updated successfully.")

                session.commit()
                #to fetch latest update or changes
                readlist = session.query(Tracker).filter_by(user_id=user_id).join(Book).all() 

            elif action == "rate_book":
                rating = float(request.POST.get("rating"))
                if 1 <= rating <= 5:
                    selected_entry.book.rating = rating
                    messages.success(request, "Book rating updated successfully.")
                    session.commit()

                else:
                    messages.error(request, "Please enter a valid rating between 1 and 5.")

                        # Confirm data was committed and updated
            return redirect("progress_tracker_page", user_id=user_id)

        # Render readlist with status and rating options
        context = {
            "readlist": readlist,
            "user_id": user_id
        }
        return render(request, "tracker_app/progress_tracker_page.html", context)

    finally:
        session.close()

# USER PROFLE LOGIC (CHANGE USERNAM OR PASSWORD, REMOVE BOOKS FROM READLIST)
def user_profile_view(request, user_id):
    session = SessionLocal()
    try:
        # Fetch the user and readlist with books preloaded
        user = session.query(User).filter_by(user_id=user_id).first()
        readlist = session.query(Tracker).filter_by(user_id=user_id).options(joinedload(Tracker.book)).all()

        if request.method == 'POST':
            # Change username
            if 'change_username' in request.POST:
                new_username = request.POST.get('new_username')
                if new_username:
                    existing_user = session.query(User).filter(User.name == new_username).first()
                    if not existing_user:
                        user.name = new_username
                        session.commit()
                        messages.success(request, "Username updated successfully.")
                    else:
                        messages.warning(request, "Username already exists. Please choose another.")

                return redirect('user_profile', user_id=user_id)

            # Change password
            elif 'change_password' in request.POST:
                new_password = request.POST.get('new_password')
                if new_password:
                    user.password = hash_password(new_password)
                    session.commit()
                    messages.success(request, "Password updated successfully.")
                else:
                    messages.warning(request, "Password cannot be empty.")

                return redirect('user_profile', user_id=user_id)

            # Remove selected books from readlist
            elif 'remove_books' in request.POST:
                selected_books = request.POST.getlist('books')
                if selected_books:  # Check if any books were selected
                    for tracker_id in selected_books:
                        book_to_remove = session.query(Tracker).filter_by(tracker_id=tracker_id, user_id=user_id).first()
                        if book_to_remove:
                            session.delete(book_to_remove)
                            messages.success(request, f"Removed '{book_to_remove.book.title}' from your readlist.")  # Success message
                    session.commit()
                else:
                    messages.warning(request, "No books were selected for removal.")  # Warning message

        # Render the profile page with user and readlist information
        return render(request, 'tracker_app/user_profile.html', {
            'user': user,
            'readlist': readlist
        })
    finally:
        session.close()

# ADMIN INTERFACE (BOOK AND USER MANAGEMENT)
def admin_user_management_view(request):
    session = SessionLocal()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username and password:
                hashed_password = hash_password(password)
                new_user = User(name=username, password=hashed_password)
                session.add(new_user)
                session.commit()
                messages.success(request, f"User '{username}' added successfully.")
            else:
                messages.warning(request, "Username and password cannot be empty.")

        elif action == 'remove':
            username = request.POST.get('username')
            user_to_remove = session.query(User).filter_by(name=username).first()
            if user_to_remove:
                session.delete(user_to_remove)
                session.commit()
                messages.success(request, f"User '{username}' removed successfully.")
            else:
                messages.warning(request, "User not found.")

    users = session.query(User).all()
    return render(request, 'tracker_app/admin_user_management.html', {'users': users})


def admin_book_management_view(request):
    session = SessionLocal()

    if request.method == 'POST':
        action = request.POST.get('action')
        book_id = request.POST.get('book_id')

        if action == 'remove':
            book_to_remove = session.query(Book).filter_by(book_id=book_id).first()
            if book_to_remove:
                session.delete(book_to_remove)
                session.commit()
                messages.success(request, f"Book '{book_to_remove.title}' removed successfully.")
            else:
                messages.warning(request, "Book not found.")

        elif action == 'edit':
            book = session.query(Book).filter_by(book_id=book_id).first()
            if book:
                # Update only if a new value is provided; otherwise, keep the old value
                title = request.POST.get('title').strip()
                authors = request.POST.get('authors').strip()
                description = request.POST.get('description').strip()
                pages = request.POST.get('pages').strip()
                rating = request.POST.get('rating').strip()

                # Update title if provided
                if title:  # Only update if not empty
                    book.title = title

                # Update authors if provided
                if authors:  # Only update if not empty
                    book.authors = authors
            
                #Update description if provided
                if description:  # Only update if not empty
                    book.description = description
                
                # Update pages if provided
                if pages:  # Check if pages is not empty and is a valid number
                    try:
                        book.pages = int(pages)
                    except ValueError:
                        messages.error(request, "Invalid value for pages. Please enter a valid number.")

                # Update rating if provided
                if rating:  # Check if rating is not empty and is a valid number
                    try:
                        book.rating = float(rating)
                    except ValueError:
                        messages.error(request, "Invalid value for rating. Please enter a valid number.")

                session.commit()
                messages.success(request, f"Book '{book.title}' updated successfully.")
            else:
                messages.warning(request, "Book not found.")

        
    # Fetching only 2000 for faster rendering books to display in the template (Remove limit to view all books)
    books = session.query(Book).limit(2000).all()
    return render(request, 'tracker_app/admin_book_management.html', {'books': books})
