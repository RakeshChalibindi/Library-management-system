# =====================================================================
# MENU MODULE
# Contains interactive terminal loops for the flat system menu.
# Collects user keyboard input, processes commands, and shows results.
# =====================================================================

from utils import clear_screen, wait_and_clear
from reports import (display_all_books, display_user_transactions, display_all_borrowed_books,
                     display_book_details, display_member_details, display_all_members,
                     display_book_search_results, display_member_search_results, display_library_stats)

def main_menu(user_manager, book_manager, transaction_manager):
    """
    Main loop for the Library Management System.
    Provides a flat list of 11 options for managing books, members, and loans:
    1. Add New Book
    2. View All Books
    3. Search Book
    4. Update Book
    5. Delete Book
    6. Register Member
    7. View Members
    8. Issue Book
    9. Return Book
    10. View Transaction History
    11. Exit
    """
    while True:
        clear_screen()
        print("=" * 50)
        print("1. Add New Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Register Member")
        print("7. View Members")
        print("8. Issue Book")
        print("9. Return Book")
        print("10. View Transaction History")
        print("11. Exit")
        print("=" * 50)
        
        choice = input("Select an option (1-11): ").strip()
        
        if choice == '1':
            print("\n--- Add New Book ---")
            title = input("Enter Title: ").strip()
            author = input("Enter Author: ").strip()
            isbn = input("Enter ISBN: ").strip()
            
            success, message = book_manager.add_book(title, author, isbn)
            print(message)
            if success:
                new_book = book_manager.books[-1]
                display_book_details(new_book)
            wait_and_clear()
            
        elif choice == '2':
            display_all_books(book_manager)
            input("\nPress Enter to return to the Main Menu...")
            
        elif choice == '3':
            print("\n--- Search Book ---")
            query = input("Enter keyword (Title, Author, ISBN, or Book ID): ").strip()
            if not query:
                print("Error: Search query cannot be blank.")
            else:
                results = book_manager.search_books(query)
                display_book_search_results(results, query)
            input("\nPress Enter to return to the Main Menu...")
            
        elif choice == '4':
            print("\n--- Update Book ---")
            display_all_books(book_manager)
            user_input = input("Enter Book ID to update (or press Enter to cancel): ").strip()
            
            if user_input == "":
                print("Operation cancelled.")
                wait_and_clear()
                continue
                
            try:
                book_id = int(user_input)
                book = book_manager.find_book_by_id(book_id)
                if not book:
                    print("Error: Book not found.")
                else:
                    print(f"\nEditing Book: '{book.title}'")
                    print("Leave fields blank and press Enter to keep current values.")
                    
                    new_title = input(f"New Title ({book.title}): ").strip()
                    new_author = input(f"New Author ({book.author}): ").strip()
                    new_isbn = input(f"New ISBN ({book.isbn}): ").strip()
                    
                    curr_status = "Available" if book.is_available else "Borrowed"
                    new_status_input = input(f"Current status: {curr_status}. Mark as Available? (y/n, press Enter to keep): ").strip().lower()
                    
                    title = new_title if new_title != "" else None
                    author = new_author if new_author != "" else None
                    isbn = new_isbn if new_isbn != "" else None
                    
                    is_available = None
                    if new_status_input in ['y', 'yes']:
                        is_available = True
                    elif new_status_input in ['n', 'no']:
                        is_available = False
                        
                    success, message = book_manager.update_book(book_id, title=title, author=author, isbn=isbn, is_available=is_available)
                    print(message)
                    if success:
                        # Refresh book status from disk
                        book = book_manager.find_book_by_id(book_id)
                        display_book_details(book)
            except ValueError:
                print("Error: Book ID must be a valid number.")
            wait_and_clear()
            
        elif choice == '5':
            print("\n--- Delete Book ---")
            display_all_books(book_manager)
            user_input = input("Enter Book ID to delete (or press Enter to cancel): ").strip()
            
            if user_input == "":
                print("Operation cancelled.")
                wait_and_clear()
                continue
                
            try:
                book_id = int(user_input)
                success, message = book_manager.remove_book(book_id)
                print(message)
            except ValueError:
                print("Error: Book ID must be a valid number.")
            wait_and_clear()
            
        elif choice == '6':
            print("\n--- Register Member ---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            
            if not username or not password:
                print("Error: Username and password cannot be blank.")
            else:
                success, message = user_manager.add_user(username, password, "Member")
                print(message)
                if success:
                    new_user = user_manager.find_user_by_username(username)
                    if new_user:
                        display_member_details(new_user)
            wait_and_clear()
            
        elif choice == '7':
            display_all_members(user_manager)
            input("\nPress Enter to return to the Main Menu...")
            
        elif choice == '8':
            print("\n--- Issue Book ---")
            display_all_books(book_manager)
            
            user_input_member = input("Enter Member (User) ID: ").strip()
            user_input_book = input("Enter Book ID: ").strip()
            
            if user_input_member == "" or user_input_book == "":
                print("Operation cancelled.")
                wait_and_clear()
                continue
                
            try:
                member_id = int(user_input_member)
                book_id = int(user_input_book)
                
                # Validate member existence
                member = user_manager.find_user_by_id(member_id)
                if not member:
                     print(f"Error: Member with ID {member_id} does not exist.")
                else:
                     success, message = transaction_manager.borrow_book(member_id, book_id)
                     print(message)
            except ValueError:
                print("Error: Member ID and Book ID must be valid numbers.")
            wait_and_clear()
            
        elif choice == '9':
            print("\n--- Return Book ---")
            
            user_input_member = input("Enter Member (User) ID: ").strip()
            if user_input_member == "":
                print("Operation cancelled.")
                wait_and_clear()
                continue
                
            try:
                member_id = int(user_input_member)
                member = user_manager.find_user_by_id(member_id)
                if not member:
                    print(f"Error: Member with ID {member_id} does not exist.")
                else:
                    display_user_transactions(transaction_manager, book_manager, member_id)
                    user_input_book = input("Enter Book ID to return: ").strip()
                    if user_input_book != "":
                        book_id = int(user_input_book)
                        success, message = transaction_manager.return_book(member_id, book_id)
                        print(message)
                    else:
                        print("Operation cancelled.")
            except ValueError:
                print("Error: Member ID must be a valid number.")
            wait_and_clear()
            
        elif choice == '10':
            print("\n--- View Transaction History & Reports ---")
            print("1. View Outstanding Loans (All currently checked out books)")
            print("2. View Specific Member Borrowing History")
            print("3. View Library Statistics & Activity Dashboard")
            sub_choice = input("Select report option (1-3): ").strip()
            
            if sub_choice == '1':
                display_all_borrowed_books(transaction_manager, book_manager, user_manager)
            elif sub_choice == '2':
                user_input_member = input("Enter Member ID: ").strip()
                if user_input_member != "":
                    try:
                        member_id = int(user_input_member)
                        member = user_manager.find_user_by_id(member_id)
                        if not member:
                            print(f"Error: Member with ID {member_id} not found.")
                        else:
                            display_user_transactions(transaction_manager, book_manager, member_id)
                    except ValueError:
                        print("Error: Member ID must be a valid number.")
                else:
                    print("Operation cancelled.")
            elif sub_choice == '3':
                display_library_stats(book_manager, user_manager, transaction_manager)
            else:
                print("Invalid report option selected.")
            input("\nPress Enter to return to the Main Menu...")
            
        elif choice == '11':
            print("Thank you for using the Library Management System. Goodbye!")
            wait_and_clear(1)
            break
            
        else:
            print("Invalid input. Please type a number between 1 and 11.")
            wait_and_clear(1)

if __name__ == "__main__":
    from main import main
    main()
