#translation
from googletrans import Translator

# Initialize the Translator object
translator = Translator()

# Function to translate text to the selected language
def translate_text(text, target_language):
    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"Error in translation: {e}")
        return text
