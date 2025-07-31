import tkinter as tk
from tkinter import messagebox, simpledialog
import database
from gtts import gTTS
import pygame
import tempfile

class WordListForm:
    def __init__(self, root, user_details, communication_form):
        self.root = root
        self.user_details = user_details
        self.communication_form = communication_form
        self.selected_word = None

        if 'id' not in self.user_details:
            raise ValueError("user_details must contain 'id'")

        self.root.title("Word List Form")
        self.root.geometry("600x600")
        self.root.configure(bg="light blue")

        self.word_entry = tk.Entry(self.root, font=("Arial", 14))
        self.word_entry.pack(pady=20)

        add_button = tk.Button(self.root, text="Add Word", font=("Arial", 14), command=self.add_word)
        add_button.pack(pady=10)

        self.word_listbox = tk.Listbox(self.root, font=("Arial", 14))
        self.word_listbox.pack(pady=10)
        self.word_listbox.bind('<<ListboxSelect>>', self.on_word_select)

        edit_button = tk.Button(self.root, text="Edit Word", font=("Arial", 14), command=self.edit_word)
        edit_button.pack(pady=5)

        remove_button = tk.Button(self.root, text="Remove Word", font=("Arial", 14), command=self.remove_word)
        remove_button.pack(pady=5)

        self.load_words()

    def load_words(self):
        user_id = self.user_details['id']
        words = database.get_words(user_id)
        self.word_listbox.delete(0, tk.END)
        for word in words:
            self.word_listbox.insert(tk.END, word)

    def add_word(self):
        word = self.word_entry.get()
        if word:
            user_id = self.user_details['id']
            database.add_word(user_id, word)
            self.load_words()
            self.word_entry.delete(0, tk.END)
            self.communication_form.update_text_box(f"Word added: {word}", 'user')
            self.communication_form.speak_text(f"Word added: {word}", self.communication_form.selected_language)
        else:
            messagebox.showwarning("Warning", "Word cannot be empty")

    def edit_word(self):
        if self.selected_word is None:
            messagebox.showwarning("Warning", "Select a word to edit")
            return

        new_word = self.word_entry.get()
        if new_word:
            user_id = self.user_details['id']
            old_word = self.selected_word
            database.update_word(user_id, old_word, new_word)
            self.load_words()
            self.word_entry.delete(0, tk.END)
            self.selected_word = None
            self.communication_form.update_text_box(f"Word updated: {new_word}", 'user')
            self.communication_form.speak_text(f"Word updated: {new_word}", self.communication_form.selected_language)
        else:
            messagebox.showwarning("Warning", "New word cannot be empty")

    def remove_word(self):
        if self.selected_word is None:
            messagebox.showwarning("Warning", "Select a word to remove")
            return

        word = self.selected_word
        user_id = self.user_details['id']
        database.remove_word(user_id, word)
        self.load_words()
        self.selected_word = None
        self.communication_form.update_text_box(f"Word removed: {word}", 'user')
        self.communication_form.speak_text(f"Word removed: {word}", self.communication_form.selected_language)

    def on_word_select(self, event):
        selected_word_index = self.word_listbox.curselection()
        if selected_word_index:
            word = self.word_listbox.get(selected_word_index)
            self.selected_word = word
            self.word_entry.delete(0, tk.END)
            self.word_entry.insert(0, word)
            self.speak_word(word)

    def speak_word(self, word):
        try:
            tts = gTTS(text=word, lang='en')
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                temp_file = f"{fp.name}.mp3"
                tts.save(temp_file)
                pygame.mixer.init()
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
        except Exception as e:
            messagebox.showerror("Error", f"Error speaking text: {str(e)}")

def open_wordlist_form(root, user_details, communication_form):
    wordlist_form_window = tk.Toplevel(root)
    app = WordListForm(wordlist_form_window, user_details, communication_form)
