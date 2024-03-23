import tkinter as tk
from tkinter import scrolledtext
import threading
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import json
import os

# Configure and initialize Gemini LLM
genai.configure(api_key="AIzaSyDiHIeAsfCOY2bhV_S1bXk4Y966xFay4s8")  # Replace with your Gemini LLM API key
model_gemini = genai.GenerativeModel('gemini-pro')

# File to store conversation history
conversation_file = "conversation_history.json"

def generate_gemini_response(prompt):
    response = model_gemini.generate_content(prompt)  # Corrected method name
    return response.text

def update_dataset(new_data):
    # Load existing dataset
    existing_data = []
    if os.path.exists(conversation_file):
        with open(conversation_file, 'r') as f:
            existing_data = json.load(f)
    
    # Append new data
    existing_data.append(new_data)

    # Write updated dataset back to file
    with open(conversation_file, 'w') as f:
        json.dump(existing_data, f, indent=4)

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
        # Initialize variables for user information
        user_info = {
            "Name": "",
            "Phone": "",
            "Address": ""
        }

        # Collect user information with Gemini LLM
        speak("Hello! Please provide your name.")
        user_input = convert_speech_to_text()
        if user_input is not None:
            user_info["Name"] = user_input

        speak("Great! Now, please provide your phone number.")
        user_input = convert_speech_to_text()
        if user_input is not None:
            user_info["Phone"] = user_input

        speak("Thank you! Finally, please provide your address.")
        user_input = convert_speech_to_text()
        if user_input is not None:
            user_info["Address"] = user_input

        # Store user information in conversation history
        update_dataset({"User Information": user_info})

        # Proceed to Gemini LLM for IT desk questions
        speak("Thank you for providing your information. Now, let's proceed to the IT desk questionnaire.")
        speak("Please answer the following questions.")
        it_desk_questions = [
            "What is the issue you are experiencing?",
            "When did the issue start?",
            "Have you tried any troubleshooting steps?",
            "What is your computer's operating system?",
            "Any additional information you would like to provide?"
        ]

        it_desk_answers = {}
        for question in it_desk_questions:
            speak(question)
            user_input = convert_speech_to_text()
            if user_input is not None:
                it_desk_answers[question] = user_input

        # Store IT desk questionnaire answers in conversation history
        update_dataset({"IT Desk Questions": it_desk_answers})

        # Display and speak Gemini LLM responses for IT desk questions
        for question, answer in it_desk_answers.items():
            gemini_response = generate_gemini_response(question + " " + answer)
            if gemini_response is not None:
                update_dataset({"Gemini LLM": gemini_response})
                output_text.insert(tk.END, "IT Question: " + question + "\n")
                output_text.insert(tk.END, "User Answer: " + answer + "\n")
                output_text.insert(tk.END, "Gemini LLM Response: " + gemini_response + "\n")
                output_text.see(tk.END)
                speak(gemini_response)

        speak("Thank you for answering the questions. We will assist you with the issue shortly.")

    # Create UI
    root = tk.Tk()
    root.title("Gemini LLM Voice Interaction")

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