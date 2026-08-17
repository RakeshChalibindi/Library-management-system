# =====================================================================
# TRANSACTIONS MODULE
# Handles the operations of borrowing and returning system books.
# Realizes database-like relationships (User ID linked to Book ID).
# =====================================================================

from file_handler import read_json_file, write_json_file
from datetime import datetime

TRANSACTIONS_FILE = 'transactions.json'

class TransactionManager:
    """
    Coordinates borrowing and returning records, tracking who borrowed what
    and when they returned it.
    """
    def __init__(self, book_manager):
        # We load saved transaction records (list of dictionaries)
        self.transactions = read_json_file(TRANSACTIONS_FILE)
        # We hold a reference to BookManager to update a book's availability status
        self.book_manager = book_manager

    def save_transactions(self):
        """
        Saves the current transaction logs to file.
        """
        write_json_file(TRANSACTIONS_FILE, self.transactions)

    def generate_next_id(self):
        """
        Generates the next unique numeric ID for a transaction entry.
        """
        if not self.transactions:
            return 1
            
        highest_id = 0
        for tx in self.transactions:
            tx_id = tx.get("transaction_id", 0)
            if tx_id > highest_id:
                highest_id = tx_id
        return highest_id + 1

    def borrow_book(self, user_id, book_id):
        """
        Attempts to borrow a book for a user.
        Checks book availability and marks the book as borrowed if successful.
        """
        # Find the book within our library list
        book = self.book_manager.find_book_by_id(book_id)
        if not book:
            return False, "Error: Book not found."
        
        # Verify book status
        if not book.is_available:
            return False, f"Error: '{book.title}' is currently borrowed by someone else."

        # Update book status (Opps interaction)
        book.is_available = False
        self.book_manager.save_books()

        # Build transaction log dictionary
        next_id = self.generate_next_id()
        borrow_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_transaction = {
            "transaction_id": next_id,
            "user_id": user_id,
            "book_id": book_id,
            "borrow_date": borrow_timestamp,
            "return_date": None  # 'None' means the book has not been returned yet
        }
        
        self.transactions.append(new_transaction)
        self.save_transactions()
        
        return True, f"Success: You have borrowed '{book.title}'."

    def return_book(self, user_id, book_id):
        """
        Processes returning a book.
        Finds the open transaction, marks return date, and sets book status back to available.
        """
        # Search for an active transaction where this user has this book and hasn't returned it yet
        active_tx = None
        for tx in self.transactions:
            if tx.get("user_id") == user_id and tx.get("book_id") == book_id and tx.get("return_date") is None:
                active_tx = tx
                break
                
        if not active_tx:
            return False, "Error: You can't return this book because no active borrowing record was found."

        # Mark the book as available again
        book = self.book_manager.find_book_by_id(book_id)
        if book:
            book.is_available = True
            self.book_manager.save_books()

        # Update transaction entry with current return timestamp
        return_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        active_tx['return_date'] = return_timestamp
        self.save_transactions()

        return True, f"Success: You returned '{book.title if book else 'the book'}'."

    def get_user_transactions(self, user_id):
        """
        Finds and returns all transaction logs for a single user ID.
        """
        user_list = []
        for tx in self.transactions:
            if tx.get("user_id") == user_id:
                user_list.append(tx)
        return user_list
        
    def get_all_transactions(self):
        """
        Returns all transaction logs in the system.
        """
        return self.transactions

if __name__ == "__main__":
    from main import main
    main()
