from library import Library
def main():
    print("\n")
    print("=" * 50)
    print("WELCOME TO CITY LIBRARY")
    print("LIBRARY MANAGEMENT SYSTEM")
    print("=" * 50)
    username = input("\nEnter Username: ")
    password = input("Enter Password: ")
    if username != "admin" or password != "1234":
        print("\nLogin failed!")
        print("Please check your username and password.")
        return
    print("\nLogin successful!")
    print("Welcome, Administrator.")
    library = Library()
    while True:
        print("\n")
        print("=" * 50)
        print("MAIN MENU")
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
        choice = input(
            "Please select an option: "
        )
        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.view_books()
        elif choice == "3":
            library.search_book()
        elif choice == "4":
            library.update_book()
        elif choice == "5":
            library.delete_book()
        elif choice == "6":
            library.add_member()
        elif choice == "7":
            library.view_members()
        elif choice == "8":
            library.issue_book()
        elif choice == "9":
            library.return_book()
        elif choice == "10":
            library.view_transactions()
        elif choice == "11":
            print("\n" + "=" * 50)
            print("Thank you for using City Library.")
            print("Have a great day!")
            print("=" * 50)
            break
        else:
            print(
                "\nInvalid option. "
                "Please select a number from 1 to 11."
            )


if __name__ == "__main__":
    main()