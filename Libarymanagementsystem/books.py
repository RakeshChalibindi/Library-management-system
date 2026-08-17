# -------------------------------------------------------------
# BOOKS MODULE
# This module demonstrates Object-Oriented Programming (OOP) concepts.
# We define a 'Book' class (the blueprint) and a 'BookManager' class 
# to coordinate a list of Book objects.
# ------------------------------------------------------------------

from file_handler import read_json_file, write_json_file

BOOKS_FILE = 'books.json'

class Book:
    """
    OOP Concept: Class representation of a Book.
    This acts as a template/blueprint for every book in the library.
    Each individual book we create from this class is an 'Object'.
    """
    def __init__(self, book_id, title, author, isbn, is_available=True):
        # Attributes representing the book properties
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = is_available

    def to_dict(self):
        """
        Helper function to turn our Book object attributes into a Python dictionary.
        This makes it easy to save the book directly to a JSON file.
        """
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_available": self.is_available
        }


class BookManager:
    """
    This class manages our collection of Book objects, loading them
    from JSON and saving updates back to the file.
    """
    def __init__(self):
        self.books = []
        self.load_books()

    def load_books(self):
        """
        Loads book list from the JSON file and converts each dictionary 
        into an actual Book object instance.
        """
        raw_data = read_json_file(BOOKS_FILE)
        self.books = []
        
        for item in raw_data:
            # We fetch fields explicitly. This is safer than **unpacking 
            # and is much easier to read and understand.
            book = Book(
                book_id=item.get("book_id"),
                title=item.get("title", ""),
                author=item.get("author", ""),
                isbn=item.get("isbn", ""),
                is_available=item.get("is_available", True)
            )
            self.books.append(book)

    def save_books(self):
        """
        Converts our list of Book objects into dictionaries and saves them to JSON.
        """
        data_to_save = []
        for book in self.books:
            data_to_save.append(book.to_dict())
        write_json_file(BOOKS_FILE, data_to_save)

    def generate_next_id(self):
        """
        Generates the next unique numeric ID for a new book.
        It finds the highest current ID and adds 1.
        """
        if not self.books:
            return 1
        
        highest_id = 0
        for book in self.books:
            if book.book_id > highest_id:
                highest_id = book.book_id
        return highest_id + 1

    def add_book(self, title, author, isbn):
        """
        Creates a new Book object and saves it in our list and JSON file.
        """
        if not title or not author or not isbn:
            return False, "Error: Book title, author, and ISBN are required!"

        next_id = self.generate_next_id()
        new_book = Book(next_id, title, author, isbn)
        self.books.append(new_book)
        self.save_books()
        return True, f"Book '{title}' added successfully with ID {next_id}."

    def remove_book(self, book_id):
        """
        Removes a book from the library.
        If the book is currently borrowed, it cannot be deleted.
        """
        book = self.find_book_by_id(book_id)
        if not book:
            return False, "Error: Book ID not found."
            
        if not book.is_available:
            return False, "Error: Cannot remove book. It is currently borrowed!"
            
        self.books.remove(book)
        self.save_books()
        return True, f"Book '{book.title}' was successfully removed."

    def find_book_by_id(self, book_id):
        """
        Helper method to find a Book object using its unique transaction/book ID.
        Returns None if not found.
        """
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None
        
    def get_all_books(self):
        """
        Returns the entire list containing all Book objects.
        """
        return self.books

    def search_books(self, query):
        """
        Searches for books whose title, author, or ISBN matches the query.
        Returns a list of matching Book objects.
        """
        results = []
        query_str = str(query).lower()
        for book in self.books:
            if (query_str in book.title.lower() or 
                query_str in book.author.lower() or 
                query_str in book.isbn.lower() or 
                query_str == str(book.book_id)):
                results.append(book)
        return results

    def update_book(self, book_id, title=None, author=None, isbn=None, is_available=None):
        """
        Updates book attributes if they are modified.
        """
        book = self.find_book_by_id(book_id)
        if not book:
            return False, "Error: Book not found."

        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if isbn is not None:
            book.isbn = isbn
        if is_available is not None:
            book.is_available = is_available

        self.save_books()
        return True, f"Book '{book.title}' (ID {book_id}) has been updated successfully."

if __name__ == "__main__":
    from main import main
    main()
