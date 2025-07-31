import tkinter as tk
from tkinter import messagebox
import shared
import database
from gtts import gTTS
import pygame
import tempfile

class AddressForm:
    def __init__(self, root, user_details, communication_form):
        self.root = root
        self.user_details = user_details
        self.communication_form = communication_form
        self.selected_address = None

        if 'id' not in self.user_details:
            raise ValueError("user_details must contain 'id'")

        self.root.title("Address Form")
        self.root.geometry("800x800")
        self.root.configure(bg="light blue")

        self.address_entry = tk.Entry(self.root, font=("Arial", 14))
        self.address_entry.pack(pady=20)

        add_button = tk.Button(self.root, text="Add Address", font=("Arial", 14), command=self.add_address)
        add_button.pack(pady=10)

        self.address_listbox = tk.Listbox(self.root, font=("Arial", 14))
        self.address_listbox.pack(pady=10)
        self.address_listbox.bind('<<ListboxSelect>>', self.on_address_select)

        edit_button = tk.Button(self.root, text="Edit Address", font=("Arial", 14), command=self.edit_address)
        edit_button.pack(pady=5)

        remove_button = tk.Button(self.root, text="Remove Address", font=("Arial", 14), command=self.remove_address)
        remove_button.pack(pady=5)

        self.load_addresses()

    def load_addresses(self):
        user_id = self.user_details['id']
        addresses = database.get_addresses(user_id)
        self.address_listbox.delete(0, tk.END)
        for address in addresses:
            self.address_listbox.insert(tk.END, address)

    def add_address(self):
        address = self.address_entry.get()
        if address:
            user_id = self.user_details['id']
            database.add_address(user_id, address)
            self.load_addresses()
            self.address_entry.delete(0, tk.END)
            self.communication_form.update_text_box(f"Address added: {address}", 'user')
            self.communication_form.speak_text(f"Address added: {address}", self.communication_form.selected_language)
        else:
            messagebox.showwarning("Warning", "Address cannot be empty")

    def edit_address(self):
        if self.selected_address is None:
            messagebox.showwarning("Warning", "Select an address to edit")
            return

        new_address = self.address_entry.get()
        if new_address:
            user_id = self.user_details['id']
            old_address = self.selected_address
            database.update_address(user_id, old_address, new_address)
            self.load_addresses()
            self.address_entry.delete(0, tk.END)
            self.selected_address = None
            self.communication_form.update_text_box(f"Address updated: {new_address}", 'user')
            self.communication_form.speak_text(f"Address updated: {new_address}", self.communication_form.selected_language)
        else:
            messagebox.showwarning("Warning", "New address cannot be empty")

    def remove_address(self):
        if self.selected_address is None:
            messagebox.showwarning("Warning", "Select an address to remove")
            return

        address = self.selected_address
        user_id = self.user_details['id']
        database.remove_address(user_id, address)
        self.load_addresses()
        self.selected_address = None
        self.communication_form.update_text_box(f"Address removed: {address}", 'user')
        self.communication_form.speak_text(f"Address removed: {address}", self.communication_form.selected_language)

    def on_address_select(self, event):
        selected_address_index = self.address_listbox.curselection()
        if selected_address_index:
            address = self.address_listbox.get(selected_address_index)
            self.selected_address = address
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, address)
            self.speak_address(address)

    def speak_address(self, address):
        try:
            # Check if the address is numeric
            if address.isdigit():
                spoken_address = ' '.join([self.number_to_word(digit) for digit in address])
            else:
                spoken_address = address

            # Convert text to speech
            tts = gTTS(text=spoken_address, lang='en')
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                tts.save(f"{fp.name}.mp3")
                pygame.mixer.init()
                pygame.mixer.music.load(f"{fp.name}.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pass

            # Update the CommunicationForm's text box with the spoken address
            self.communication_form.update_text_box(address, 'outside')

        except Exception as e:
            messagebox.showerror("Error", f"Error speaking text: {str(e)}")

    def number_to_word(self, digit):
        """Helper method to convert a digit to its word representation."""
        number_words = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
        }
        return number_words.get(digit, '')

def open_address_form(root, user_details, communication_form):
    address_form_window = tk.Toplevel(root)
    app = AddressForm(address_form_window, user_details, communication_form)
