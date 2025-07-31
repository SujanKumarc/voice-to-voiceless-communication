#food_from.py
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import pygame
from gtts import gTTS
import os

class FoodForm:
    def __init__(self, root, user_details, communication_form):
        self.root = root
        self.user_details = user_details
        self.communication_form = communication_form
        self.root.title("Food Form")
        self.root.configure(bg="light blue")

        # Create widgets for the food form
        content_frame = tk.Frame(self.root, bg="light blue")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(content_frame, text="Food Options", font=("Arial", 24, "bold"), bg="light blue").grid(row=0, column=0, columnspan=3, pady=10)

        # Load and resize images for buttons using Pillow
        self.images = {
            "Hot Drink": ImageTk.PhotoImage(Image.open("hot_drink.png").resize((150, 150))),  # Resize image to fit button
            "Cool Drink": ImageTk.PhotoImage(Image.open("cool_drink.png").resize((150, 150))),
            "Breakfast": ImageTk.PhotoImage(Image.open("breakfast.png").resize((150, 150))),
            "Meals": ImageTk.PhotoImage(Image.open("meals.png").resize((150, 150))),
            "Dinner": ImageTk.PhotoImage(Image.open("dinner.png").resize((150, 150))),
            "Snacks": ImageTk.PhotoImage(Image.open("snacks.png").resize((150, 150))),
            "Fruits": ImageTk.PhotoImage(Image.open("fruits.png").resize((150, 150))),
            "Dessert": ImageTk.PhotoImage(Image.open("dessert.png").resize((150, 150)))
        }

        # Define food-based buttons and their grid positions
        button_texts = ["Hot Drink", "Cool Drink", "Breakfast", "Meals", "Dinner", "Snacks", "Fruits", "Dessert"]
        num_columns = 3  # Number of buttons per row

        for index, text in enumerate(button_texts):
            row = (index // num_columns) + 1  # Start from row 1 to avoid overlap with the header
            column = index % num_columns
            button = tk.Button(content_frame, text=text, font=("Arial", 16), command=lambda t=text: self.food_selected(t),
                               image=self.images.get(text), compound="top", relief="raised", bg="lightgrey", borderwidth=2,
                               width=150, height=150)  # Set button size
            button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Adjust column weights to ensure buttons expand properly
        for col in range(num_columns):
            content_frame.grid_columnconfigure(col, weight=1)

        # Adjust row weights to ensure buttons expand properly
        for row in range(1, (len(button_texts) // num_columns) + 2):
            content_frame.grid_rowconfigure(row, weight=1)

    def food_selected(self, food_category):
        # Prompt the user for a specific food item
        food_item = simpledialog.askstring("Input", f"Please enter the specific item for {food_category.lower()}:")
        
        if food_item:
            self.create_phrase(food_category, food_item)
            self.root.destroy()  # Close the form after selection
            

    def create_phrase(self, food_category, food_item):
        phrases = {
            "kn": {
                "Hot Drink": f"ನನಗೆ {food_item} ಬಿಸಿ ಪಾನೀಯ ಬೇಕು",
                "Cool Drink": f"ನನಗೆ {food_item} ತಂಪು ಪಾನೀಯ ಬೇಕು",
                "Breakfast": f"ನನಗೆ {food_item} ತಿಂಡಿ ಬೇಕು",
                "Meals": f"ನನಗೆ {food_item} ಊಟ ಬೇಕು",
                "Dinner": f"ನನಗೆ {food_item} ರಾತ್ರಿ ಊಟ ಬೇಕು",
                "Snacks": f"ನನಗೆ {food_item} ಸ್ನ್ಯಾಕ್ಸ್ ಬೇಕು",
                "Fruits": f"ನನಗೆ {food_item} ಹಣ್ಣು ಬೇಕು",
                "Dessert": f"ನನಗೆ {food_item} ಸಿಹಿ ಬೇಕು"
            },
            "hi": {
                "Hot Drink": f"मुझे {food_item} गरम पानी चाहिए",
                "Cool Drink": f"मुझे {food_item} ठंडा पानी चाहिए",
                "Breakfast": f"मुझे {food_item} नाश्ता चाहिए",
                "Meals": f"मुझे {food_item} खाना चाहिए",
                "Dinner": f"मुझे {food_item} रात का खाना चाहिए",
                "Snacks": f"मुझे {food_item} स्नैक्स चाहिए",
                "Fruits": f"मुझे {food_item} फल चाहिए",
                "Dessert": f"मुझे {food_item} मिठाई चाहिए"
            },
            "en": {
                "Hot Drink": f"I want {food_item} as a hot drink",
                "Cool Drink": f"I want {food_item} as a cool drink",
                "Breakfast": f"I want {food_item} for breakfast",
                "Meals": f"I want {food_item} for meals",
                "Dinner": f"I want {food_item} for dinner",
                "Snacks": f"I want {food_item} for snacks",
                "Fruits": f"I want {food_item} as fruits",
                "Dessert": f"I want {food_item} for dessert"
            }
        }

        language_code = self.communication_form.selected_language
        phrase = phrases.get(language_code, {}).get(food_category, f"I want {food_item} as {food_category.lower()}")

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

def open_food_form(root, user_details, communication_form):
    food_form_window = tk.Toplevel(root)
    app = FoodForm(food_form_window, user_details, communication_form)
