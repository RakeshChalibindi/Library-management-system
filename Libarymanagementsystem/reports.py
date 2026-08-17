# =-----------------------------------------------------------------------
# REPORTS MODULE
# Contains utility functions to display tables in the terminal.
# Uses alignment features of Python strings to draw nice columns.
# -------------------------------------------------------------------------

def display_all_books(book_manager):
    """
    Prints a formatted table of all books in the library system.
    """
    books = book_manager.get_all_books()
    
    print("===="*25)
    print(" LATEST LIBRARY BOOKS")
    print("=="* 50)
    
    if not books:
        print("   No books are currently in the library catalog.")
        print("=")
        return
        
    # Table headers: left aligned using '<' formatter
    print(f"{'ID':<5} | {'Book Title':<30} | {'Author':<20} | {'ISBN':<15} | {'Status':<10} |")
    print("-" * 100)
    
    for book in books:
        status_text = "Available" if book.is_available else "Borrowed"
        
        # Trim titles or authors if they are too long for our column widths
        title_trimmed = book.title[:28]
        author_trimmed = book.author[:18]
        
        print(f"{book.book_id:<5} | {title_trimmed:<30} | {author_trimmed:<20} | {book.isbn:<15} | {status_text:<10} |" )
        
    print("=="* 50)

def display_user_transactions(transaction_manager, book_manager, user_id):
    """
    Prints a borrow/return history table for a specific user ID.
    """
    transactions = transaction_manager.get_user_transactions(user_id)
    
    print(f"\n===")
    print(f" BORROWING HISTORY FOR USER ID: {user_id}")
    print(f"===")
    
    if not transactions:
        print("   No transactions recorded for this user yet.")
        print("==")
        return
        
    print(f"{'TX ID':<6} | {'Book Title':<30} | {'Borrow Date':<20} | {'Return Date':<20}")
    print("-" * 82)
    
    for tx in transactions:
        book = book_manager.find_book_by_id(tx.get("book_id"))
        book_title = book.title if book else "Unknown Book"
        
        return_date = tx.get("return_date")
        if not return_date:
            return_date = "Still Borrowed"
            
        print(f"{tx.get('transaction_id'):<6} | {book_title[:28]:<30} | {tx.get('borrow_date'):<20} | {return_date:<20}")
        
    print("===")
    
def display_all_borrowed_books(transaction_manager, book_manager, user_manager):
    """
    Prints a general status list of every book currently checked out 
    and who has it.
    """
    transactions = transaction_manager.get_all_transactions()
    
    # Filter active loans (loans that don't have a return date yet)
    active_loans = []
    for tx in transactions:
        if tx.get("return_date") is None:
            active_loans.append(tx)
            
    print("\n====")
    print(" LOG OF ALL OUTSTANDING LOANS")
    print("=====")
    
    if not active_loans:
        print("   There are currently no borrowed books in the system.")
        print("====")
        return
        
    print(f"{'Book ID':<8} | {'Book Title':<30} | {'Borrowed By (User)':<20} | {'Borrow Date':<20}")
    print("-" * 82)
    
    for tx in active_loans:
        book = book_manager.find_book_by_id(tx.get("book_id"))
        book_title = book.title if book else "Deleted Book"
        
        # Find which user profile matches the ID using a simple loop
        borrower_name = "Unknown member"
        user_id = tx.get("user_id")
        for user in user_manager.users:
            if user.user_id == user_id:
                borrower_name = f"{user.username} (ID: {user_id})"
                break
                
        print(f"{tx.get('book_id'):<8} | {book_title[:28]:<30} | {borrower_name:<20} | {tx.get('borrow_date'):<20}")
        
    print("====")

def display_book_details(book):
    """
    Prints a details card of a single book.
    """
    print("\n====")
    print(" NEWLY ADDED BOOK DETAILS")
    print("===")
    print(f"   Book ID    : {book.book_id}")
    print(f"   Title      : {book.title}")
    print(f"   Author     : {book.author}")
    print(f"   ISBN       : {book.isbn}")
    print(f"   Status     : {'Available' if book.is_available else 'Borrowed'}")
    print("=====")

def display_member_details(member):
    """
    Prints a details card of a single member.
    """
    print("\n=======")
    print(" NEWLY REGISTERED MEMBER ")
    print("===")
    print(f"   User ID    : {member.user_id}")
    print(f"   Username   : {member.username}")
    print(f"   Role       : {member.role}")
    print(f"   Last Login : {member.last_login}")
    print("===")

def display_all_members(user_manager):
    """
    Prints a table of all registered library members.
    """
    members = user_manager.get_all_members()
    print("\n==")
    print("  REGISTERED LIBRARY MEMBERS")
    print("===")
    if not members:
        print("   No member accounts are currently registered.")
        print("===")
        return
    print(f"{'ID':<5} | {'Username':<30} | {'Role':<15} | {'Last Login Time':<20}")
    print("-" * 82)
    for member in members:
        print(f"{member.user_id:<5} | {member.username[:28]:<30} | {member.role:<15} | {member.last_login:<20}")
    print("====")

def display_book_search_results(books, query):
    """
    Prints search results for books.
    """
    print("\n====")
    print(f" BOOK SEARCH RESULTS FOR: '{query}'")
    print("==")
    if not books:
        print("   No books found matching the search criteria.")
        print("===")
        return
    print(f"{'ID':<5} | {'Book Title':<30} | {'Author':<20} | {'ISBN':<15} | {'Status':<10}")
    print("-" * 82)
    for book in books:
        status_text = "Available" if book.is_available else "Borrowed"
        print(f"{book.book_id:<5} | {book.title[:28]:<30} | {book.author[:18]:<20} | {book.isbn:<15} | {status_text:<10}")
    print("====")

def display_member_search_results(members, query):
    """
    Prints search results for members.
    """
    print("\n=====")
    print(f"   MEMBER SEARCH RESULTS FOR: '{query}'")
    print("=======")
    if not members:
        print("   No members found matching the search criteria.")
        print("==")
        return
    print(f"{'ID':<5} | {'Username':<30} | {'Role':<15} | {'Last Login Time':<20}")
    print("-" * 82)
    for member in members:
        print(f"{member.user_id:<5} | {member.username[:28]:<30} | {member.role:<15} | {member.last_login:<20}")
    print("=====")

def display_library_stats(book_manager, user_manager, transaction_manager):
    """
    Displays statistics about total books, members, active readers, and active reader loans.
    """
    all_books = book_manager.get_all_books()
    all_members = user_manager.get_all_members()
    transactions = transaction_manager.get_all_transactions()
    
    # Calculate statistics
    total_books = len(all_books)
    available_books = sum(1 for b in all_books if b.is_available)
    borrowed_books_count = total_books - available_books
    total_members = len(all_members)
    
    # Members currently reading (distinct user IDs with active checkouts)
    active_borrowed_txs = [tx for tx in transactions if tx.get("return_date") is None]
    active_reader_ids = {tx.get("user_id") for tx in active_borrowed_txs}
    active_readers_count = len(active_reader_ids)
    
    print("\n===")
    print("  LIBRARY DASHBOARD & ACTIVITY STATS")
    print("==")
    print(f"   Total Books in Catalog : {total_books:<10} | Available Books  : {available_books}")
    print(f"   Total Registered Members: {total_members:<10} | Books Checked out : {borrowed_books_count}")
    print(f"   Active Members Reading  : {active_readers_count:<10} | Out of Total Members")
    print("=")
    
    print("\n   --- CURRENT ACTIVE READERS & THEIR BOOKS ---")
    if not active_borrowed_txs:
        print("   There are currently no members reading or borrowing books.")
    else:
        print("-" * 82)
        print(f"{'Member Username':<25} | {'Book Title':<30} | {'Borrow Date':<20}")
        print("-" * 82)
        for tx in active_borrowed_txs:
            book = book_manager.find_book_by_id(tx.get("book_id"))
            book_title = book.title if book else "Unknown Book"
            
            # Find member username
            username = "Unknown Member"
            for u in user_manager.users:
                if u.user_id == tx.get("user_id"):
                    username = f"{u.username} (ID: {u.user_id})"
                    break
            print(f"{username[:23]:<25} | {book_title[:28]:<30} | {tx.get('borrow_date'):<20}")
    print("==")

if __name__ == "__main__":
    from main import main
    main()
