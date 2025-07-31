#feeling_from.py
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import pygame
from gtts import gTTS
import os

class FeelingForm:
    def __init__(self, root, user_details, communication_form):
        self.root = root
        self.user_details = user_details
        self.communication_form = communication_form
        self.root.title("Feeling Form")
        self.root.configure(bg="light blue")

        # Create widgets for the feeling form
        content_frame = tk.Frame(self.root, bg="light blue")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(content_frame, text="Feeling Options", font=("Arial", 24, "bold"), bg="light blue").grid(row=0, column=0, columnspan=3, pady=10)

        # Load and resize images for buttons using Pillow
        self.images = {
            "Happy": ImageTk.PhotoImage(Image.open("happy.png").resize((150, 150))),  # Resize image to fit button
            "Sad": ImageTk.PhotoImage(Image.open("sad.png").resize((150, 150))),
            "Anger": ImageTk.PhotoImage(Image.open("anger.png").resize((150, 150))),
            "Fear": ImageTk.PhotoImage(Image.open("fear.png").resize((150, 150))),
            "Love": ImageTk.PhotoImage(Image.open("love.png").resize((150, 150))),
            "Surprise": ImageTk.PhotoImage(Image.open("surprise.png").resize((150, 150))),
            "Disgust": ImageTk.PhotoImage(Image.open("disgust.png").resize((150, 150))),
            "Pride": ImageTk.PhotoImage(Image.open("pride.png").resize((150, 150)))
        }

        # Define feeling-based buttons and their grid positions
        button_texts = ["Happy", "Sad", "Anger", "Fear", "Love", "Surprise", "Disgust", "Pride"]
        num_columns = 3  # Number of buttons per row

        for index, text in enumerate(button_texts):
            row = (index // num_columns) + 1  # Start from row 1 to avoid overlap with the header
            column = index % num_columns
            button = tk.Button(content_frame, text=text, font=("Arial", 16), command=lambda t=text: self.feeling_selected(t),
                               image=self.images.get(text), compound="top", relief="raised", bg="lightgrey", borderwidth=2,
                               width=150, height=150)  # Set button size
            button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Adjust column weights to ensure buttons expand properly
        for col in range(num_columns):
            content_frame.grid_columnconfigure(col, weight=1)

        # Adjust row weights to ensure buttons expand properly
        for row in range(1, (len(button_texts) // num_columns) + 2):
            content_frame.grid_rowconfigure(row, weight=1)

    def feeling_selected(self, feeling):
        # Prompt the user for more details about the feeling
        feeling_detail = simpledialog.askstring("Input", f"Please describe why you are feeling {feeling.lower()}:")

        if feeling_detail:
            self.create_phrase(feeling, feeling_detail)
            self.root.destroy()  # Close the form after selection

    def create_phrase(self, feeling, feeling_detail):
        phrases = {
            "kn": {
                "Happy": f"ನಾನು ಸಂತೋಷದಿಂದ ಇರುವೆನು {feeling_detail}",
                "Sad": f"ನಾನು ವಿಷಾದದಿಂದ ಇರುವೆನು {feeling_detail}",
                "Anger": f"ನಾನು ಕೋಪದಿಂದ ಇರುವೆನು {feeling_detail}",
                "Fear": f"ನಾನು ಭಯದಿಂದ ಇರುವೆನು {feeling_detail}",
                "Love": f"ನಾನು ಪ್ರೀತಿಯಿಂದ ಇರುವೆನು {feeling_detail}",
                "Surprise": f"ನಾನು ಆಶ್ಚರ್ಯದಿಂದ ಇರುವೆನು {feeling_detail}",
                "Disgust": f"ನಾನು ಅಸಹ್ಯದಿಂದ ಇರುವೆನು {feeling_detail}",
                "Pride": f"ನಾನು ಹೆಮ್ಮೆಯಿಂದ ಇರುವೆನು {feeling_detail}"
            },
            "hi": {
                "Happy": f"मैं {feeling_detail} से खुश हूँ",
                "Sad": f"मैं {feeling_detail} से दुखी हूँ",
                "Anger": f"मैं {feeling_detail} से नाराज हूँ",
                "Fear": f"मैं {feeling_detail} से डरा हुआ हूँ",
                "Love": f"मैं {feeling_detail} से प्यार करता हूँ",
                "Surprise": f"मैं {feeling_detail} से हैरान हूँ",
                "Disgust": f"मैं {feeling_detail} से घृणा करता हूँ",
                "Pride": f"मैं {feeling_detail} पर गर्व महसूस करता हूँ"
            },
            "en": {
                "Happy": f"I am feeling happy because {feeling_detail}",
                "Sad": f"I am feeling sad because {feeling_detail}",
                "Anger": f"I am feeling angry because {feeling_detail}",
                "Fear": f"I am feeling fearful because {feeling_detail}",
                "Love": f"I am feeling love because {feeling_detail}",
                "Surprise": f"I am feeling surprised because {feeling_detail}",
                "Disgust": f"I am feeling disgusted because {feeling_detail}",
                "Pride": f"I am feeling proud because {feeling_detail}"
            }
        }

        language_code = self.communication_form.selected_language
        phrase = phrases.get(language_code, {}).get(feeling, f"I am feeling {feeling.lower()} because {feeling_detail}")

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

def open_feeling_form(root, user_details, communication_form):
    feeling_form_window = tk.Toplevel(root)
    app = FeelingForm(feeling_form_window, user_details, communication_form)
