class Member:

    def __init__(self, member_id, name, email, phone):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone

    def display_member(self):
        print("\nMember Details")
        print("Member ID    :", self.member_id)
        print("Member Name  :", self.name)
        print("Email Address:", self.email)
        print("Phone Number :", self.phone)
        print("")