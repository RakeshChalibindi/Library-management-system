from file_handler import FileHandler
from book import Book
from member import Member
from datetime import datetime


class Library:

    def __init__(self):

        self.file_handler = FileHandler()

        self.book_file = "books.json"
        self.member_file = "members.json"
        self.transaction_file = "transactions.json"

    # ---------------- ADD BOOK ----------------

    def add_book(self):

        print("\n========== ADD NEW BOOK ==========")

        book_id = input("Enter Book ID       : ")
        title = input("Enter Book Title    : ")
        author = input("Enter Author Name   : ")
        category = input("Enter Book Category : ")

        try:
            quantity = int(
                input("Enter Available Qty : ")
            )

        except ValueError:
            print("\nPlease enter a valid number.")
            return

        books = self.file_handler.read_file(
            self.book_file
        )

        for book in books:

            if book["book_id"] == book_id:

                print("\nBook ID already exists.")
                return

        book = Book(
            book_id,
            title,
            author,
            category,
            quantity
        )

        book_data = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "category": book.category,
            "quantity": book.quantity
        }

        books.append(book_data)

        self.file_handler.write_file(
            self.book_file,
            books
        )

        print("\nBook added successfully!")
        print("The book is now available in the library.")


    # ---------------- VIEW BOOKS ----------------

    def view_books(self):

        print("\n========== ALL BOOKS ==========")

        books = self.file_handler.read_file(
            self.book_file
        )

        if len(books) == 0:

            print("\nNo books are currently available.")
            return

        for book_data in books:

            book = Book(
                book_data["book_id"],
                book_data["title"],
                book_data["author"],
                book_data["category"],
                book_data["quantity"]
            )

            book.display_book()


    # ---------------- SEARCH BOOK ----------------

    def search_book(self):

        print("\n========== SEARCH BOOK ==========")

        search = input(
            "Enter Book Title or Author Name: "
        ).lower()

        books = self.file_handler.read_file(
            self.book_file
        )

        found = False

        for book in books:

            if (
                search in book["title"].lower()
                or
                search in book["author"].lower()
            ):

                print("\n========== Search Result ==========")
                print("Book ID       :", book["book_id"])
                print("Book Title    :", book["title"])
                print("Author Name   :", book["author"])
                print("Book Category :", book["category"])
                print("Available Qty :", book["quantity"])
                print("===================================")

                found = True

        if found == False:

            print("\nNo matching book was found.")


    # ---------------- UPDATE BOOK ----------------

    def update_book(self):

        print("\n========== UPDATE BOOK ==========")

        book_id = input(
            "Enter Book ID to Update: "
        )

        books = self.file_handler.read_file(
            self.book_file
        )

        found = False

        for book in books:

            if book["book_id"] == book_id:

                print("\nEnter Updated Book Details")

                book["title"] = input(
                    "Enter New Book Title    : "
                )

                book["author"] = input(
                    "Enter New Author Name   : "
                )

                book["category"] = input(
                    "Enter New Book Category : "
                )

                try:

                    book["quantity"] = int(
                        input("Enter New Available Qty : ")
                    )

                except ValueError:

                    print("\nPlease enter a valid number.")
                    return

                found = True
                break

        if found:

            self.file_handler.write_file(
                self.book_file,
                books
            )

            print("\nBook details updated successfully.")

        else:

            print("\nBook ID was not found.")


    # ---------------- DELETE BOOK ----------------

    def delete_book(self):

        print("\n========== DELETE BOOK ==========")

        book_id = input(
            "Enter Book ID to Delete: "
        )

        books = self.file_handler.read_file(
            self.book_file
        )

        new_books = []

        found = False

        for book in books:

            if book["book_id"] == book_id:

                found = True

            else:

                new_books.append(book)

        if found:

            self.file_handler.write_file(
                self.book_file,
                new_books
            )

            print("\nBook deleted successfully.")

        else:

            print("\nBook ID was not found.")


    # ---------------- ADD MEMBER ----------------

    def add_member(self):

        print("\n========== REGISTER MEMBER ==========")

        member_id = input("Enter Member ID    : ")
        name = input("Enter Member Name  : ")
        email = input("Enter Email Address : ")
        phone = input("Enter Phone Number  : ")

        members = self.file_handler.read_file(
            self.member_file
        )

        for member in members:

            if member["member_id"] == member_id:

                print("\nMember ID already exists.")
                return

        member = Member(
            member_id,
            name,
            email,
            phone
        )

        member_data = {
            "member_id": member.member_id,
            "name": member.name,
            "email": member.email,
            "phone": member.phone
        }

        members.append(member_data)

        self.file_handler.write_file(
            self.member_file,
            members
        )

        print("\nMember registered successfully!")


    # ---------------- VIEW MEMBERS ----------------

    def view_members(self):

        print("\n========== REGISTERED MEMBERS ==========")

        members = self.file_handler.read_file(
            self.member_file
        )

        if len(members) == 0:

            print("\nNo members are registered.")
            return

        for member_data in members:

            member = Member(
                member_data["member_id"],
                member_data["name"],
                member_data["email"],
                member_data["phone"]
            )

            member.display_member()


    # ---------------- ISSUE BOOK ----------------

    def issue_book(self):

        print("\n========== ISSUE BOOK ==========")

        book_id = input("Enter Book ID   : ")
        member_id = input("Enter Member ID : ")

        books = self.file_handler.read_file(
            self.book_file
        )

        members = self.file_handler.read_file(
            self.member_file
        )

        book_found = False
        member_found = False

        for book in books:

            if book["book_id"] == book_id:

                book_found = True

                if book["quantity"] <= 0:

                    print("\nThis book is currently unavailable.")
                    return

        for member in members:

            if member["member_id"] == member_id:

                member_found = True

        if book_found == False:

            print("\nBook ID was not found.")
            return

        if member_found == False:

            print("\nMember ID was not found.")
            return

        for book in books:

            if book["book_id"] == book_id:

                book["quantity"] -= 1

        self.file_handler.write_file(
            self.book_file,
            books
        )

        transaction = {

            "book_id": book_id,

            "member_id": member_id,

            "action": "Issued",

            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        transactions = self.file_handler.read_file(
            self.transaction_file
        )

        transactions.append(transaction)

        self.file_handler.write_file(
            self.transaction_file,
            transactions
        )

        print("\nBook issued successfully!")
        print("Please return the book after use.")


    # ---------------- RETURN BOOK ----------------

    def return_book(self):

        print("\n========== RETURN BOOK ==========")

        book_id = input("Enter Book ID   : ")
        member_id = input("Enter Member ID : ")

        books = self.file_handler.read_file(
            self.book_file
        )

        found = False

        for book in books:

            if book["book_id"] == book_id:

                book["quantity"] += 1

                found = True
                break

        if found == False:

            print("\nBook ID was not found.")
            return

        self.file_handler.write_file(
            self.book_file,
            books
        )

        transaction = {

            "book_id": book_id,

            "member_id": member_id,

            "action": "Returned",

            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        transactions = self.file_handler.read_file(
            self.transaction_file
        )

        transactions.append(transaction)

        self.file_handler.write_file(
            self.transaction_file,
            transactions
        )

        print("\nBook returned successfully!")
        print("Thank you for returning the book.")


    # ---------------- VIEW TRANSACTIONS ----------------

    def view_transactions(self):

        print("\n========== TRANSACTION HISTORY ==========")

        transactions = self.file_handler.read_file(
            self.transaction_file
        )

        if len(transactions) == 0:

            print("\nNo transactions have been recorded.")
            return

        for transaction in transactions:

            print("\n----------------------------------------")

            print(
                "Book ID   :",
                transaction["book_id"]
            )

            print(
                "Member ID :",
                transaction["member_id"]
            )

            print(
                "Action    :",
                transaction["action"]
            )

            print(
                "Date      :",
                transaction["date"]
            )

            print("----------------------------------------")