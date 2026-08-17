# MAIN MODULE ------------------------------------------------------
# The starting point of the application. It acts as the driver script.
# Handles initialization of managers and launches the flat main menu.
# -----------------------------------------------------------------------------

from members import UserManager
from books import BookManager
from transactions import TransactionManager
from menu import main_menu

def main():
    # Initialize the core managers
    user_manager = UserManager()
    book_manager = BookManager()
    transaction_manager = TransactionManager(book_manager)

    # Launch the flat main menu (options 1-11)
    main_menu(user_manager, book_manager, transaction_manager)

if __name__ == "__main__":
    main()
