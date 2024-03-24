import tkinter as tk
from tkinter import scrolledtext
import threading
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import json
from gtts import gTTS
from googletrans import Translator
import os
import json

MAIN_DOMAIN=""
LANG=""

with open('./data/data.json', 'r') as domain:
    domainData = json.load(domain)

# Configure and initialize Gemini LLM
genai.configure(api_key="AIzaSyDiHIeAsfCOY2bhV_S1bXk4Y966xFay4s8")  # Replace with your Gemini LLM API key
model_gemini = genai.GenerativeModel('gemini-pro')

# File to store conversation history
conversation_file = "./data/conversation_history.json"


def translate_to_hindi(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='hi')
    return translated.text

def generate_hindi_audio(text):
    # Specify language (Hindi)
    language = 'hi'

    # Create gTTS object with the text and language
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the audio to a file
    tts.save("output.mp3")

    # Specify the path to the audio file
    audio_file_path = r"\./output\.mp3"
    
    # Construct the command with proper escaping
    # command = f'Start-Process -FilePath "{audio_file_path}" -Wait -WindowStyle Minimized'
    command ="start output.mp3 -WindowStyle Hidden"

    os.system(command)

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
            recognizer.pause_threshold = 0.7
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
        # start_button['state'] = 'disabled'
        # stop_button['state'] = 'normal'
        threading.Thread(target=start_listening).start()
        
    def onClickAction(domain):
        # setattr(root, 'MAIN_DOMAIN', domain)
        global MAIN_DOMAIN
        MAIN_DOMAIN = domain
        on_start_button()
        
    def changeLanguage(lang):
        global LANG
        LANG = lang

    def start_listening():
        # Initialize variables for user information
        user_info = {
            "Name": "",
            "Phone": "",
            "Address": ""
        }

        # Collect user information with Gemini LLM
        output_text.insert(tk.END , "ASSISTANT: " + "Hello! Please provide your name." + "\n\n")
        output_text.see(tk.END)
        
        if LANG == "hin":
            hindi_op = translate_to_hindi("Hello! Please provide your name.")
            generate_hindi_audio(hindi_op)
            os.system("rm .\output.mp3")
        else:
            speak("Hello! Please provide your name.")
            
        user_input = convert_speech_to_text()
        if user_input is not None:
            output_text.insert(tk.END, "USER: " + user_input + "\n\n")
            output_text.see(tk.END)
            user_info["Name"] = user_input
            

        output_text.insert(tk.END, "ASSISTANT: " + "Great! Now, please provide your phone number." + "\n\n")
        output_text.see(tk.END)
        
        if LANG == "hin":
            hindi_op = translate_to_hindi("Great! Now, please provide your phone number.")
            generate_hindi_audio(hindi_op)
            os.system("rm .\output.mp3")
        else:
            speak("Great! Now, please provide your phone number.")
            
        user_input = convert_speech_to_text()
        if user_input is not None:
            output_text.insert(tk.END, "USER: " + user_input + "\n\n")
            output_text.see(tk.END)
            user_info["Phone"] = user_input

        output_text.insert(tk.END, "ASSISTANT: " + "Thank you! Finally, please provide your address." + "\n\n")
        output_text.see(tk.END)
        
        if LANG == "hin":
            hindi_op = translate_to_hindi("Thank you! Finally, please provide your address.")
            generate_hindi_audio(hindi_op)
            os.system("rm .\output.mp3")
        else:
            speak("Thank you! Finally, please provide your address.")
            
        user_input = convert_speech_to_text()
        if user_input is not None:
            output_text.insert(tk.END, "USER: " + user_input + "\n\n")
            output_text.see(tk.END)
            user_info["Address"] = user_input

        # Store user information in conversation history
        update_dataset({"User Information": user_info})

        # Proceed to Gemini LLM for IT desk questions
        output_text.insert(tk.END, "ASSISTANT: " + f"Thank you for providing your information. Now, let's proceed to the {MAIN_DOMAIN} questionnaire." + "\n\n")
        output_text.see(tk.END)
        
        if LANG == "hin":
            hindi_op = translate_to_hindi(f"Thank you for providing your information. Now, let's proceed to the {MAIN_DOMAIN} questionnaire.")
            generate_hindi_audio(hindi_op)
            os.system("rm .\output.mp3")
        else:
            speak(f"Thank you for providing your information. Now, let's proceed to the {MAIN_DOMAIN} questionnaire.")

        output_text.insert(tk.END, "ASSISTANT: " + "Please answer the following questions." + "\n\n")
        output_text.see(tk.END)
        
        if LANG == "hin":
            hindi_op = translate_to_hindi("Please answer the following questions.")
            generate_hindi_audio(hindi_op)
            os.system("rm .\output.mp3")
        else:
            speak("Please answer the following questions.")

        it_desk_answers = {}
        print(MAIN_DOMAIN)
        for question in domainData[MAIN_DOMAIN]:
            if LANG == "hin":
                hindi_op = translate_to_hindi(question)
                generate_hindi_audio(hindi_op)
                os.system("rm .\output.mp3")
            else:
                speak(question)
            output_text.insert(tk.END, "ASSISTANT: " + question + "\n\n")
            output_text.see(tk.END)
            user_input = convert_speech_to_text()
            output_text.insert(tk.END, "USER: " + user_input + "\n\n")
            output_text.see(tk.END)
            if user_input is not None:
                it_desk_answers[question] = user_input

        # Store IT desk questionnaire answers in conversation history
        update_dataset({"IT Desk Questions": it_desk_answers})

        # Display and speak Gemini LLM responses for IT desk questions
        for question, answer in it_desk_answers.items():
            gemini_response = generate_gemini_response(question + " " + answer)
            gemini_response_formated = gemini_response.replace("*", "")
            if gemini_response is not None:
                update_dataset({"Gemini LLM": gemini_response})
                output_text.insert(tk.END, "IT Question: " + question + "\n")
                output_text.insert(tk.END, "User Answer: " + answer + "\n")
                output_text.insert(tk.END, "Gemini LLM Response: " + gemini_response_formated + "\n")
                output_text.see(tk.END)
                speak(gemini_response_formated)

        speak("Thank you for answering the questions. We will assist you with the issue shortly.")

    # Create UI
    root = tk.Tk()
    root.title("CVA - 302FOUND")
    
    output_text = scrolledtext.ScrolledText(root, width=60, height=20)
    output_text.grid(row=0, columnspan=4)

    it_button = tk.Button(root, text="IT Help Desk", command=lambda: onClickAction("IT"))
    it_button.grid(row=1, column=0, pady=20)

    manf_button = tk.Button(root, text="Manufacturing", command=lambda: onClickAction("Manufacturing"))
    manf_button.grid(row=1, column=1, pady=20)
    
    network_button = tk.Button(root, text="Network", command=lambda: onClickAction("IT"))
    network_button.grid(row=1, column=2, pady=20)
    
    service_button = tk.Button(root, text="Service", command=lambda: onClickAction("IT"))
    service_button.grid(row=1, column=3, pady=20)

    eng_button = tk.Button(root, text="English", command=lambda: changeLanguage("eng"))
    eng_button.grid(row=2, columnspan=2, pady=20)
    
    hindi_button = tk.Button(root, text="Hindi", command=lambda: changeLanguage("hin")) 
    hindi_button.grid(row=2, column=2, columnspan=2, pady=20)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    speech_to_text()