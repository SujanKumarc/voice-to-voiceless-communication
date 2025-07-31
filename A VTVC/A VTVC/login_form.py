import tkinter as tk
from tkinter import messagebox
import database
import registration_form  # Ensure this import matches the filename of your registration form

def open_login_form():
    import communication_form  # Import inside the function to avoid circular import
    root = tk.Tk()
    app = LoginForm(root, communication_form.open_communication_form)
    root.mainloop()

class LoginForm:
    def __init__(self, root, open_communication_form):
        self.root = root
        self.root.title("Login Page")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")

        login_frame = tk.Frame(root, bg="light blue", padx=20, pady=20)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(login_frame, text="LOGIN", font=("Arial", 24, "bold"), bg="light blue").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(login_frame, text="Username:", font=("Arial", 16), bg="light blue").grid(row=1, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(login_frame, font=("Arial", 16))
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(login_frame, text="Password:", font=("Arial", 16), bg="light blue").grid(row=2, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(login_frame, show='*', font=("Arial", 16))
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Adding extra space between the password field and buttons
        login_frame.grid_rowconfigure(3, minsize=20)  # Adds vertical space between the password field and the buttons

        # Configure the grid to center the buttons
        login_frame.grid_columnconfigure(0, weight=1)
        login_frame.grid_columnconfigure(1, weight=1)

        # Set button size and font to smaller
        button_font = ("Arial", 14)  # Smaller font size
        button_width = 12  # Smaller button width

        login_button = tk.Button(login_frame, text="Login", font=button_font, width=button_width, command=self.validate_login)
        login_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        register_button = tk.Button(login_frame, text="Register", font=button_font, width=button_width, command=self.open_registration_form)
        register_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.open_communication_form = open_communication_form

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_details = database.validate_login(username, password)
        if user_details:
            self.root.destroy()
            self.open_communication_form(user_details)
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def open_registration_form(self):
        self.root.destroy()  # Close the login form
        registration_form.open_registration_form()  # Open the registration form

if __name__ == "__main__":
    open_login_form()
