import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import tkinter as tk
from tkinter import messagebox

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen Function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        window.update()
        audio = recognizer.listen(source, phrase_time_limit=5)
    
    try:
        command = recognizer.recognize_google(audio)
        status_label.config(text="You said: " + command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        status_label.config(text="Didn't understand.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        status_label.config(text="Network error.")
        return ""

# Command Handler
def handle_command():
    command = listen()
    
    if 'hello' in command:
        response = "Hello! Nice to meet you."
    elif 'time' in command:
        response = f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
    elif 'date' in command:
        response = f"Today's date is {datetime.date.today().strftime('%B %d, %Y')}"
    elif 'search for' in command:
        query = command.replace("search for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        response = f"Searching Google for {query}"
    elif 'wikipedia' in command:
        query = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            response = f"According to Wikipedia: {summary}"
        except:
            response = "Sorry, I couldn't find that on Wikipedia."
    elif 'exit' in command or 'stop' in command:
        response = "Goodbye!"
        speak(response)
        window.destroy()
        return
    elif command:
        response = "I don't know how to do that yet."
    else:
        return
    
    response_label.config(text=response)
    speak(response)

# GUI Setup
window = tk.Tk()
window.title("Voice Assistant")
window.geometry("500x300")
window.configure(bg="#f0f0f0")

title_label = tk.Label(window, text="Voice Assistant", font=("Helvetica", 20), bg="#f0f0f0")
title_label.pack(pady=10)

status_label = tk.Label(window, text="Click the button and speak...", font=("Helvetica", 12), bg="#f0f0f0", fg="blue")
status_label.pack(pady=5)

listen_button = tk.Button(window, text="🎤 Speak", font=("Helvetica", 14), command=handle_command, bg="#4CAF50", fg="white", padx=20, pady=10)
listen_button.pack(pady=20)

response_label = tk.Label(window, text="", wraplength=400, font=("Helvetica", 12), bg="#f0f0f0", justify="center")
response_label.pack(pady=10)

exit_button = tk.Button(window, text="Exit", command=window.quit, font=("Helvetica", 12), bg="red", fg="white")
exit_button.pack(pady=10)

window.mainloop()
