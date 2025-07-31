#text_to_speech
import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to start listening and recognizing speech
def start_listening(text_box):
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            translated_text = translate_text(text, selected_language)
            text_box.insert(tk.END, translated_text + '\n', 'user')
            speak_text(translated_text)
        except Exception as e:
            print(f"Error: {e}")
            text_box.insert(tk.END, "Sorry, I couldn't understand that.\n", 'outside')

# Function to focus and respond to text input
def focus_and_answer(text_box):
    text_box.insert(tk.END, "User is typing...\n", 'outside')
    text_box.focus_set()

