import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import pygame
from gtts import gTTS
import os

class ColorForm:
    def __init__(self, root, user_details, communication_form):
        self.root = root
        self.user_details = user_details
        self.communication_form = communication_form
        self.root.title("Color Form")
        self.root.configure(bg="light blue")

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

        # Create widgets for the color form
        content_frame = tk.Frame(self.root, bg="light blue")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(content_frame, text="Color Options", font=("Arial", 24, "bold"), bg="light blue").grid(row=0, column=0, columnspan=3, pady=10)

        # Load and resize images for buttons using Pillow
        self.images = self.load_images()

        # Define color-based buttons and their grid positions
        button_texts = ["Red", "Orange", "Yellow", "Green", "Blue", "Pink", "Brown", "Grey", "Black", "White", "Peach"]
        num_columns = 3  # Number of buttons per row

        for index, text in enumerate(button_texts):
            row = (index // num_columns) + 1  # Start from row 1 to avoid overlap with the header
            column = index % num_columns
            button = tk.Button(content_frame, text=text, font=("Arial", 12), command=lambda t=text: self.color_selected(t),
                               image=self.images.get(text), compound="top", relief="raised", bg="lightgrey", borderwidth=2,
                               width=120, height=120)  # Set button size
            button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Adjust column weights to ensure buttons expand properly
        for col in range(num_columns):
            content_frame.grid_columnconfigure(col, weight=1)

        # Adjust row weights to ensure buttons expand properly
        for row in range(1, (len(button_texts) // num_columns) + 2):
            content_frame.grid_rowconfigure(row, weight=1)

    def load_images(self):
        images = {}
        default_image = ImageTk.PhotoImage(Image.new('RGB', (120, 120), color='gray'))

        colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Pink", "Brown", "Grey", "Black", "White", "Peach"]
        for color in colors:
            try:
                images[color] = ImageTk.PhotoImage(Image.open(f"{color.lower()}.png").resize((120, 120)))
            except FileNotFoundError:
                images[color] = default_image

        return images

    def color_selected(self, color):
        # Prompt the user for more details about the color
        color_detail = simpledialog.askstring("Input", f"Please describe what you think about {color.lower()}:")

        if color_detail:
            self.create_phrase(color, color_detail)
            self.root.destroy()  # Close the form after selection

    def create_phrase(self, color, color_detail):
        phrases = {
            "kn": {
                "Red": f"ನಾನು ಕೆಂಪು ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "Orange": f"ನಾನು ಕಿತ್ತಳೆ ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "Yellow": f"ನಾನು ಹಳದಿ ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "Green": f"ನಾನು ಹಸಿರು ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "Blue": f"ನಾನು ನೀಲಿ ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "Pink": f"ನಾನು ಗುಲಾಬಿ ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "Brown": f"ನಾನು ಕಂದು ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "Grey": f"ನಾನು ಬೂದು ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "Black": f"ನಾನು ಕಪ್ಪು ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "White": f"ನಾನು ಬಿಳಿ ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}",
                "Peach": f"ನಾನು ಪೀಚ್ ಬಣ್ಣವನ್ನು ಇಷ್ಟಪಡುತ್ತೇನೆ {color_detail}"
            },
            "hi": {
                "Red": f"मुझे लाल रंग पसंद है {color_detail}",
                "Orange": f"मुझे नारंगी रंग पसंद है {color_detail}",
                "Yellow": f"मुझे पीला रंग पसंद है {color_detail}",
                "Green": f"मुझे हरा रंग पसंद है {color_detail}",
                "Blue": f"मुझे नीला रंग पसंद है {color_detail}",
                "Pink": f"मुझे गुलाबी रंग पसंद है {color_detail}",
                "Brown": f"मुझे भूरा रंग पसंद है {color_detail}",
                "Grey": f"मुझे ग्रे रंग पसंद है {color_detail}",
                "Black": f"मुझे काला रंग पसंद है {color_detail}",
                "White": f"मुझे सफेद रंग पसंद है {color_detail}",
                "Peach": f"मुझे पीच रंग पसंद है {color_detail}"
            },
            "en": {
                "Red": f"I like the color red because {color_detail}",
                "Orange": f"I like the color orange because {color_detail}",
                "Yellow": f"I like the color yellow because {color_detail}",
                "Green": f"I like the color green because {color_detail}",
                "Blue": f"I like the color blue because {color_detail}",
                "Pink": f"I like the color pink because {color_detail}",
                "Brown": f"I like the color brown because {color_detail}",
                "Grey": f"I like the color grey because {color_detail}",
                "Black": f"I like the color black because {color_detail}",
                "White": f"I like the color white because {color_detail}",
                "Peach": f"I like the color peach because {color_detail}"
            }
        }

        language_code = self.communication_form.selected_language
        phrase = phrases.get(language_code, {}).get(color, f"I like the color {color.lower()} because {color_detail}")

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

def open_color_form(root, user_details, communication_form):
    color_form_window = tk.Toplevel(root)
    app = ColorForm(color_form_window, user_details, communication_form)
