import google.generativeai as genai
import speech_recognition as sr
import json
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
        
    # Introduction
    introduction = "Hello! I'm here to assist you. You can ask me anything or give me commands. To exit, simply say 'exit'. Let's get started!"
    print(introduction)
    speak(introduction)

    while True:
        user_input = convert_speech_to_text()
        if user_input:
            response = generate_response(user_input)
            print("Gemini:", response)
            speak(response)

            # Optionally, you can add a condition to exit the loop
            if user_input.lower() == "exit":
                speak("Goodbye!")
                break

if __name__ == "__main__":
    speech_to_text()
