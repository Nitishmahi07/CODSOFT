import re
import json

class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {"name": self.name, "phone": self.phone, "email": self.email}

class ContactBook:
    def __init__(self):
        self.contacts = {}
        self.load_contacts()

    def add_contact(self, contact):
        if contact.phone in self.contacts:
            print("Error: Contact with this phone number already exists.")
        else:
            self.contacts[contact.phone] = contact
            print("Contact added successfully.")
            self.save_contacts()

    def view_contacts(self):
        return self.contacts.values()

    def search_contact(self, search_term):
        results = []
        search_term = search_term.lower()
        for contact in self.contacts.values():
            if search_term in contact.name.lower() or search_term in contact.phone:
                results.append(contact)
        return results

    def update_contact(self, old_phone, new_contact):
        if old_phone in self.contacts:
            del self.contacts[old_phone]
            self.contacts[new_contact.phone] = new_contact
            print("Contact updated successfully.")
            self.save_contacts()
        else:
            print("Contact not found.")

    def delete_contact(self, phone):
        if phone in self.contacts:
            del self.contacts[phone]
            print("Contact deleted successfully.")
            self.save_contacts()
        else:
            print("Contact not found.")

    def save_contacts(self):
        with open('contacts.json', 'w') as f:
            json.dump({phone: contact.to_dict() for phone, contact in self.contacts.items()}, f)

    def load_contacts(self):
        try:
            with open('contacts.json', 'r') as f:
                contacts_data = json.load(f)
                self.contacts = {phone: Contact(**contact) for phone, contact in contacts_data.items()}
        except FileNotFoundError:
            self.contacts = {}

def is_valid_phone(phone):
    return phone.isdigit()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def display_menu():
    print("\nContact Book Menu:")
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

def handle_add_contact(contact_book):
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")

    if not name or not phone:
        print("Name and phone number are required.")
    elif not is_valid_phone(phone):
        print("Invalid phone number. Must be numeric.")
    elif email and not is_valid_email(email):
        print("Invalid email format.")
    else:
        contact = Contact(name, phone, email)
        contact_book.add_contact(contact)

def handle_view_contacts(contact_book):
    contacts = contact_book.view_contacts()
    if contacts:
        for contact in contacts:
            print(f"Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}")
    else:
        print("No contacts available.")

def handle_search_contact(contact_book):
    search_term = input("Enter name or phone number to search: ")
    results = contact_book.search_contact(search_term)
    if results:
        for contact in results:
            print(f"Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}")
    else:
        print("No contacts found.")

def handle_update_contact(contact_book):
    phone = input("Enter the phone number of the contact to update: ")
    if phone in contact_book.contacts:
        name = input("Enter new name: ")
        new_phone = input("Enter new phone number: ")
        email = input("Enter new email: ")

        if not name or not new_phone:
            print("Name and phone number are required.")
        elif not is_valid_phone(new_phone):
            print("Invalid phone number. Must be numeric.")
        elif email and not is_valid_email(email):
            print("Invalid email format.")
        else:
            new_contact = Contact(name, new_phone, email)
            contact_book.update_contact(phone, new_contact)
    else:
        print("Contact not found.")

def handle_delete_contact(contact_book):
    phone = input("Enter the phone number of the contact to delete: ")
    if phone in contact_book.contacts:
        contact_book.delete_contact(phone)
    else:
        print("Contact not found.")

def main():
    contact_book = ContactBook()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            handle_add_contact(contact_book)
        elif choice == '2':
            handle_view_contacts(contact_book)
        elif choice == '3':
            handle_search_contact(contact_book)
        elif choice == '4':
            handle_update_contact(contact_book)
        elif choice == '5':
            handle_delete_contact(contact_book)
        elif choice == '6':
            print("Exiting the Contact Book.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
