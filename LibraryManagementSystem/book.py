class Book:
    def __init__(self, book_id, title, author, category, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity
    def display_book(self):
        print("Book details")
        print("Book ID  :", self.book_id)
        print("Title    :", self.title)
        print("Author   :", self.author)
        print("Category :", self.category)
        print("Quantity :", self.quantity)

