#greeting_form
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import pygame
from gtts import gTTS
import os

class GreetingForm:
    def __init__(self, root, user_details, communication_form):
        self.root = root
        self.user_details = user_details
        self.communication_form = communication_form
        self.root.title("Greeting Form")
        self.root.configure(bg="light blue")

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

        # Create widgets for the greeting form
        content_frame = tk.Frame(self.root, bg="light blue")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(content_frame, text="Greeting Options", font=("Arial", 24, "bold"), bg="light blue").grid(row=0, column=0, columnspan=2, pady=10)

        # Load and resize images for buttons using Pillow
        self.images = self.load_images()

        # Define greeting-based buttons and their grid positions
        button_texts = ["Morning", "Afternoon", "Evening", "General"]
        for index, text in enumerate(button_texts):
            row = index // 2 + 1
            column = index % 2
            button = tk.Button(content_frame, text=text, font=("Arial", 12), command=lambda t=text: self.greeting_selected(t),
                               image=self.images.get(text), compound="top", relief="raised", bg="lightgrey", borderwidth=2,
                               width=120, height=120)  # Set button size
            button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Adjust column weights to ensure buttons expand properly
        for col in range(2):
            content_frame.grid_columnconfigure(col, weight=1)

        # Adjust row weights to ensure buttons expand properly
        for row in range(1, 3):
            content_frame.grid_rowconfigure(row, weight=1)

    def load_images(self):
        images = {}
        default_image = ImageTk.PhotoImage(Image.new('RGB', (120, 120), color='gray'))

        greetings = ["Morning", "Afternoon", "Evening", "General"]
        for greeting in greetings:
            try:
                images[greeting] = ImageTk.PhotoImage(Image.open(f"{greeting.lower()}.png").resize((120, 120)))
            except FileNotFoundError:
                images[greeting] = default_image

        return images

    def greeting_selected(self, greeting):
        # Prompt the user for more details about the greeting
        greeting_detail = simpledialog.askstring("Input", f"Please enter your {greeting.lower()} greeting message:")

        if greeting_detail:
            self.create_phrase(greeting, greeting_detail)
            self.root.destroy()  # Close the form after selection

    def create_phrase(self, greeting, greeting_detail):
        phrases = {
            "kn": {
                "Morning": f"ಶುಭೋದಯ {greeting_detail}",
                "Afternoon": f"ಶುಭ ಮಧ್ಯಾಹ್ನ {greeting_detail}",
                "Evening": f"ಶುಭ ಸಂಜೆ {greeting_detail}",
                "General": f"ನಮಸ್ಕಾರ {greeting_detail}"
            },
            "hi": {
                "Morning": f"सुप्रभात {greeting_detail}",
                "Afternoon": f"शुभ अपराह्न {greeting_detail}",
                "Evening": f"शुभ संध्या {greeting_detail}",
                "General": f"नमस्ते {greeting_detail}"
            },
            "en": {
                "Morning": f"Good Morning {greeting_detail}",
                "Afternoon": f"Good Afternoon {greeting_detail}",
                "Evening": f"Good Evening {greeting_detail}",
                "General": f"Hello {greeting_detail}"
            }
        }

        language_code = self.communication_form.selected_language
        phrase = phrases.get(language_code, {}).get(greeting, f"{greeting} {greeting_detail}")

        if phrase:
            self.speak(phrase, language_code)
            self.communication_form.update_text_box(phrase, 'user')

    def speak(self, text, language_code):
        try:
            tts = gTTS(text=text, lang=language_code)
            temp_audio = "temp.mp3"
            tts.save(temp_audio)

            # Use pygame to play the audio
            pygame.mixer.music.load(temp_audio)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # wait for the music to finish playing
                pygame.time.Clock().tick(10)

            pygame.mixer.music.unload()
            os.remove(temp_audio)
        except Exception as e:
            print(f"Error speaking text: {e}")

def open_greeting_form(root, user_details, communication_form):
    greeting_form_window = tk.Toplevel(root)
    app = GreetingForm(greeting_form_window, user_details, communication_form)
