import tkinter as tk
import database
from login_form import open_login_form

def main():
    # Initialize the database
    database.initialize_database()

    

    # Check if registration is complete
    if not database.is_registration_complete():
        import registration_form
        app = registration_form.RegistrationForm(root, open_login_form)
    else:
        open_login_form()

    

if __name__ == "__main__":
    main()
