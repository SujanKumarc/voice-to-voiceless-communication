#language_function.py
from language_function import translate_text
from googletrans import Translator
#languagae_function.py
# Function to set language and highlight selected button
def set_language(language_code, button):
    global selected_language

    selected_language = language_code
    for lang_code, btn in language_buttons.items():
        if lang_code == language_code:
            btn.config(bg="green")
        else:
            btn.config(bg="turquoise")

    print(f"Language set to: {language_code}")

    translator = Translator()

# Function to translate text to the selected language
def translate_text(text, target_language):
    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"Error in translation: {e}")
        return text
