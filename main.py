import tkinter as tk
from tkinter import scrolledtext
import threading
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

genai.configure(api_key="AIzaSyDiHIeAsfCOY2bhV_S1bXk4Y966xFay4s8")  # Replace with your API key
model = genai.GenerativeModel('gemini-pro')

def generate_response(input_text):
    response = model.generate_content(input_text)
    return response.text

def speech_to_text():
    recognizer = sr.Recognizer()

    def convert_speech_to_text():
        with sr.Microphone() as source:
            print("Please say something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print(f"Sorry, an error occurred: {e}")

    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty("voice", voices[1].id)
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 1)
        engine.say(text)
        engine.runAndWait()

    def on_start_button():
        start_button['state'] = 'disabled'
        stop_button['state'] = 'normal'
        threading.Thread(target=start_listening).start()

    def on_stop_button():
        stop_button['state'] = 'disabled'
        start_button['state'] = 'normal'

    def start_listening():
        while True:
            user_input = convert_speech_to_text()
            if user_input:
                response = generate_response(user_input)
                output_text.insert(tk.END, "User: " + user_input + "\n")
                output_text.insert(tk.END, "Gemini: " + response + "\n")
                output_text.see(tk.END)
                speak(response)

                # Optionally, you can add a condition to exit the loop
                if user_input.lower() == "exit":
                    speak("Goodbye!")
                    break

    # Create UI
    root = tk.Tk()
    root.title("Gemini Voice Interaction")

    start_button = tk.Button(root, text="Start Listening", command=on_start_button)
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop Listening", command=on_stop_button, state='disabled')
    stop_button.pack(pady=5)

    output_text = scrolledtext.ScrolledText(root, width=60, height=20)
    output_text.pack(padx=10, pady=10)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    speech_to_text()