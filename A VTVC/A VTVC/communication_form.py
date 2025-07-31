import tkinter as tk
from tkinter import simpledialog
import speech_recognition as sr
from gtts import gTTS
import os
import pygame
from googletrans import Translator
from food_form import open_food_form
from feeling_form import open_feeling_form
from greeting_form import open_greeting_form
from color_form import open_color_form
from address_form import open_address_form
from wordlist_form import open_wordlist_form

class CommunicationForm:
    def __init__(self, root, user_details):
        self.root = root
        self.root.title("Voice to Voiceless Communication")
        self.root.state('zoomed')
        self.root.configure(bg="light blue")

        self.user_details = user_details

        # Initialize pygame mixer
        pygame.mixer.init()

        # Create a frame for the side navigation menu
        side_nav_frame = tk.Frame(self.root, bg="turquoise", width=300)
        side_nav_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Add buttons to the side navigation menu
        tk.Label(side_nav_frame, text="Language", font=("Arial", 16, "bold"), bg="turquoise", fg="black").pack(pady=10)

        def create_language_button(text, language_code):
            button = tk.Button(side_nav_frame, text=text, font=("Arial", 14), command=lambda: self.set_language(language_code, button), bg="turquoise", relief="flat")
            button.pack(fill=tk.X, padx=10, pady=5)
            self.language_buttons[language_code] = button

        self.language_buttons = {}
        create_language_button("Kannada", "kn")
        create_language_button("English", "en")
        create_language_button("Hindi", "hi")

        tk.Label(side_nav_frame, text="My Voice", font=("Arial", 16, "bold"), bg="turquoise", fg="black").pack(pady=10)

        food_button = tk.Button(side_nav_frame, text="Food", font=("Arial", 14), command=lambda: open_food_form(self.root, self.user_details, self), bg="turquoise", relief="flat")
        food_button.pack(fill=tk.X, padx=10, pady=5)

        feeling_button = tk.Button(side_nav_frame, text="Feeling", font=("Arial", 14), command=self.open_feeling_form, bg="turquoise", relief="flat")
        feeling_button.pack(fill=tk.X, padx=10, pady=5)

        greeting_button = tk.Button(side_nav_frame, text="Greeting", font=("Arial", 14), command=self.open_greeting_form, bg="turquoise", relief="flat")
        greeting_button.pack(fill=tk.X, padx=10, pady=5)

        color_button = tk.Button(side_nav_frame, text="Color", font=("Arial", 14), command=self.open_color_form, bg="turquoise", relief="flat")
        color_button.pack(fill=tk.X, padx=10, pady=5)

        address_button = tk.Button(side_nav_frame, text="Address", font=("Arial", 14), command=self.open_address_form, bg="turquoise", relief="flat")
        address_button.pack(fill=tk.X, padx=10, pady=5)

        word_list_button = tk.Button(side_nav_frame, text="Word List", font=("Arial", 14), command=self.open_wordlist_form, bg="turquoise", relief="flat")
        word_list_button.pack(fill=tk.X, padx=10, pady=5)

        # Create widgets for the communication form
        content_frame = tk.Frame(self.root, bg="light blue")
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        welcome_message1 = f"Hi {self.user_details['first_name']}!!"
        welcome_message2 = "Welcome to Voice to Voiceless Communication"
        tk.Label(content_frame, text=welcome_message1, font=("Arial", 24, "bold"), bg="light blue").pack(pady=10)
        tk.Label(content_frame, text=welcome_message2, font=("Arial", 24, "bold"), bg="light blue").pack(pady=10)

        self.text_box = tk.Text(content_frame, font=("Arial", 14), height=20, width=80)
        self.text_box.pack(pady=10)

        # Define tags for different background colors
        self.text_box.tag_configure('user', background='lightblue', foreground='black')
        self.text_box.tag_configure('outside', background='lightgreen', foreground='black')

        button_frame = tk.Frame(content_frame, bg="light blue")
        button_frame.pack(pady=10)

        listen_button = tk.Button(button_frame, text="Listen", font=("Arial", 16), command=self.start_listening)
        listen_button.pack(side=tk.LEFT, padx=10)

        answer_button = tk.Button(button_frame, text="Answer", font=("Arial", 16), command=self.focus_and_answer)
        answer_button.pack(side=tk.LEFT, padx=10)

        self.recognizer = sr.Recognizer()
        self.selected_language = 'en'

    def set_language(self, language_code, selected_button):
        self.selected_language = language_code

        # Update the appearance of the selected button and reset others
        for code, button in self.language_buttons.items():
            if code == language_code:
                button.config(relief="sunken", bg="lightgreen")
            else:
                button.config(relief="flat", bg="turquoise")

    def open_feeling_form(self):
        open_feeling_form(self.root, self.user_details, self)

    def open_greeting_form(self):
        open_greeting_form(self.root, self.user_details, self)

    def open_color_form(self):
        open_color_form(self.root, self.user_details, self)

    def open_address_form(self):
        open_address_form(self.root, self.user_details, self)

    def open_wordlist_form(self):
        open_wordlist_form(self.root, self.user_details, self)

    def translate_text(self, text, target_language):
        translator = Translator()
        try:
            translated = translator.translate(text, dest=target_language)
            return translated.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def start_listening(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio, language=self.selected_language)
                print(f"Recognized: {text}")
                translated_text = self.translate_text(text, self.selected_language)
                self.update_text_box(f"Outsider: {translated_text}", 'outside')
                self.speak_text(translated_text, self.selected_language)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                self.update_text_box("Outsider: Sorry, I couldn't understand that.", 'outside')
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                self.update_text_box("Outsider: Could not request results from Google Speech Recognition service.", 'outside')

    def focus_and_answer(self):
        # Prompt the user for input
        user_input = simpledialog.askstring("Input", "Please enter your response:")
        
        if user_input:
            # Translate the user input to the selected language
            translated_user_input = self.translate_text(user_input, self.selected_language)

            # Update the text box with the translated user input
            self.update_text_box(f"You: {translated_user_input}", 'user')

            # Speak the translated user input
            self.speak_text(translated_user_input, self.selected_language)
        else:
            self.update_text_box("You: No input provided.", 'user')

    def speak_text(self, text, language_code):
        try:
            tts = gTTS(text=text, lang=language_code)
            temp_audio = "temp.mp3"
            tts.save(temp_audio)
            pygame.mixer.music.load(temp_audio)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
            pygame.mixer.music.unload()  # Unload the music after playing
            os.remove(temp_audio)  # Now it's safe to remove the file
        except Exception as e:
            print(f"Error speaking text: {e}")

    def update_text_box(self, text, tag='outside'):
        print(f"Updating text box with: {text}")
        self.text_box.insert(tk.END, text + '\n', tag)
        self.text_box.see(tk.END)

def open_communication_form(user_details):
    root = tk.Tk()
    app = CommunicationForm(root, user_details)
    root.mainloop()
