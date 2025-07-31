import tkinter as tk
from tkinter import messagebox
import database
import login_form  # Import the login_form module
import re  # For regular expression-based password validation

def open_registration_form():
    root = tk.Tk()
    app = RegistrationForm(root)
    root.mainloop()

class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Page")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")

        registration_frame = tk.Frame(root, bg="light green", padx=20, pady=20)
        registration_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(registration_frame, text="REGISTER", font=("Arial", 24, "bold"), bg="light green").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(registration_frame, text="First Name:", font=("Arial", 16), bg="light green").grid(row=1, column=0, padx=10, pady=5)
        self.first_name_entry = tk.Entry(registration_frame, font=("Arial", 16))
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(registration_frame, text="Last Name:", font=("Arial", 16), bg="light green").grid(row=2, column=0, padx=10, pady=5)
        self.last_name_entry = tk.Entry(registration_frame, font=("Arial", 16))
        self.last_name_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(registration_frame, text="Age:", font=("Arial", 16), bg="light green").grid(row=3, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(registration_frame, font=("Arial", 16))
        self.age_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(registration_frame, text="Gender:", font=("Arial", 16), bg="light green").grid(row=4, column=0, padx=10, pady=5)
        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
        gender_frame = tk.Frame(registration_frame, bg="light green")
        gender_frame.grid(row=4, column=1, padx=10, pady=5)
        tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male", font=("Arial", 14), bg="light green").pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female", font=("Arial", 14), bg="light green").pack(side=tk.LEFT)

        tk.Label(registration_frame, text="Username:", font=("Arial", 16), bg="light green").grid(row=5, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(registration_frame, font=("Arial", 16))
        self.username_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(registration_frame, text="Password:", font=("Arial", 16), bg="light green").grid(row=6, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(registration_frame, show='*', font=("Arial", 16))
        self.password_entry.grid(row=6, column=1, padx=10, pady=5)

        register_button = tk.Button(registration_frame, text="Register", font=("Arial", 16), command=self.register_user)
        register_button.grid(row=7, column=0, columnspan=2, pady=10)

    def validate_password(self, password):
        # Ensure password has at least 8 characters, 1 uppercase letter, and 1 special character
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character."
        return True, ""

    def register_user(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_var.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if all fields are filled
        if not all([first_name, last_name, age, gender, username, password]):
            messagebox.showerror("Registration Error", "All fields are required!")
            return

        # Validate the password
        is_valid, message = self.validate_password(password)
        if not is_valid:
            messagebox.showerror("Password Error", message)
            return

        # Check if the username is already taken
        if database.is_username_taken(username):
            messagebox.showerror("Registration Error", "Username already exists! Please choose a different username.")
            return

        # Save the user in the database
        database.register_user(username, password, first_name, last_name, age, gender)
        messagebox.showinfo("Registration Success", "Registration successful!")
        self.root.destroy()
        login_form.open_login_form()  # Redirect back to login form after successful registration

if __name__ == "__main__":
    open_registration_form()
