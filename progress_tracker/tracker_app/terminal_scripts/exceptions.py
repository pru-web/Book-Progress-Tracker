# Custom Exceptions used in login credentials verification on main_menu.py 
#  Used to verify book existence in admin_book_management.py and menu_page.py

class InvalidCredentialsException(Exception):
    def __init__(self, message="Invalid username or password!"):
        self.message = message
        super().__init__(self.message)

class BookNotFoundException(Exception):
    """Raised when a book does not exist in the database."""
    def __init__(self, message="The requested book does not exist. Please check the book ID and try again."):
        self.message = message
        super().__init__(self.message)