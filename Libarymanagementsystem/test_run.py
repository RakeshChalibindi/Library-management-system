# =====================================================================
# INTEGRATION TESTING SCRIPT
# This script simulates core actions like registering users, adding books,
# borrowing, and returning to verify that the modular code behaves correctly.
# =====================================================================

from members import UserManager
from books import BookManager
from transactions import TransactionManager
import os

print("--- Testing Refactored Library Management System ---")

# Clean up existing test data to start fresh
if os.path.exists('data'):
    for f in os.listdir('data'):
        try:
            os.remove(os.path.join('data', f))
        except PermissionError:
            pass

# 1. Initialize Managers
print("\n[Step 1] Initializing manager classes...")
user_manager = UserManager()
book_manager = BookManager()
transaction_manager = TransactionManager(book_manager)

# By default, load_users() creates an 'admin' account if data is empty.
print(f"Registered users in database: {[u.username for u in user_manager.users]}")

# 2. Add Books
print("\n[Step 2] Adding test books to catalog...")
book_manager.add_book("The Hobbit", "J.R.R. Tolkien", "123456789")
book_manager.add_book("1984", "George Orwell", "987654321")
print(f"Books currently in catalog: {[b.title for b in book_manager.get_all_books()]}")

# 3. Add a Member User and authenticate
print("\n[Step 3] Registering and authenticating a new member user...")
success, msg = user_manager.add_user("testuser", "password123")
print(f"Add User Result: {msg}")

test_user = user_manager.find_user_by_username("testuser")
if test_user:
    print(f"User check: Successfully retrieved member '{test_user.username}' (ID: {test_user.user_id})")

# Authenticate test
auth_user = user_manager.authenticate("testuser", "password123")
print(f"Authentication test: {'PASSED' if auth_user is not None else 'FAILED'}")

# 4. Borrowing flow test
print("\n[Step 4] Testing borrowing flow...")
book_id_to_borrow = 1
success, msg = transaction_manager.borrow_book(test_user.user_id, book_id_to_borrow)
print(f"Borrow Action: {msg}")

borrowed_book = book_manager.find_book_by_id(book_id_to_borrow)
print(f"Book 1 Availability status (Expected False): {borrowed_book.is_available}")

# 5. Returning flow test
print("\n[Step 5] Testing returning flow...")
success, msg = transaction_manager.return_book(test_user.user_id, book_id_to_borrow)
print(f"Return Action: {msg}")

returned_book = book_manager.find_book_by_id(book_id_to_borrow)
print(f"Book 1 Availability status (Expected True): {returned_book.is_available}")

# 6. Testing Search
print("\n[Step 6] Testing Book & Member search...")
from reports import display_book_search_results, display_member_search_results, display_library_stats

# Book search
search_query_book = "Hobbit"
search_books_res = book_manager.search_books(search_query_book)
print(f"Book search query '{search_query_book}' matched: {[b.title for b in search_books_res]}")
display_book_search_results(search_books_res, search_query_book)

# Member search
search_query_user = "test"
search_members_res = user_manager.search_members(search_query_user)
print(f"Member search query '{search_query_user}' matched: {[u.username for u in search_members_res]}")
display_member_search_results(search_members_res, search_query_user)

# 7. Testing login timestamps
print("\n[Step 7] Testing login tracking...")
print(f"User default last login: {test_user.last_login}")
# Authenticating again to trigger last_login update
auth_user = user_manager.authenticate("testuser", "password123")
print(f"User last login after success: {auth_user.last_login if auth_user else 'Auth Failed'}")

# Borrow book again to show in active stats
transaction_manager.borrow_book(test_user.user_id, book_id_to_borrow)

# 8. Testing Library statistics dashboard
print("\n[Step 8] Testing Library Statistics report display...")
display_library_stats(book_manager, user_manager, transaction_manager)

# 9. Testing finding user by ID
print("\n[Step 9] Testing find_user_by_id...")
found_user = user_manager.find_user_by_id(test_user.user_id)
print(f"Found User ID {test_user.user_id}: {found_user.username if found_user else 'Not Found'}")

# 10. Testing Update Book
print("\n[Step 10] Testing update_book...")
success, msg = book_manager.update_book(1, title="The Hobbit Redux", author="J.R.R. Tolkien Sr.", isbn="999888777", is_available=True)
print(f"Update Book Result: {msg}")
updated_book = book_manager.find_book_by_id(1)
print(f"Updated Book Title (Expected 'The Hobbit Redux'): {updated_book.title if updated_book else 'Not Found'}")
print(f"Updated Book Author (Expected 'J.R.R. Tolkien Sr.'): {updated_book.author if updated_book else 'Not Found'}")
print(f"Updated Book ISBN (Expected '999888777'): {updated_book.isbn if updated_book else 'Not Found'}")

print("\n--- Test Completed Successfully! ---")
