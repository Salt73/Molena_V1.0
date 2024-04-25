import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import os

# Initialize speech recognizer and TTS engine
r = sr.Recognizer()
engine = pyttsx3.init()

listening = False  # Flag to control listening loop

def hear():
    global listening
    while listening:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
                my_txt = r.recognize_google(audio, language="ar-SA, en-US")
                return my_txt
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
        
    return ""

def write(text):
    file_path = "My_Words.txt"
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")

def on_hear_button_click():
    global listening
    listening = True
    text = hear()
    if text:
        text_display.config(state=tk.NORMAL)
        text_display.insert(tk.END, text + "\n")
        text_display.config(state=tk.DISABLED)
        write(text)
        print("wrote text")

def on_stop_button_click():
    global listening
    listening = False  # Stop listening
    print("Stopped listening to the microphone")

def on_delete_button_click():
    file_path = "My_Words.txt"
    try:
        with open(file_path, "w") as f:
            f.write("")  # Write an empty string to clear the file
        
        messagebox.showinfo("Success", "Old words deleted successfully!")
        text_display.config(state=tk.NORMAL)
        text_display.delete("1.0", tk.END)
        text_display.config(state=tk.DISABLED)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")

root = tk.Tk()
root.title("Speech Recognition")

# Create text display
text_display = tk.Text(root, height=10, width=50)
text_display.pack(pady=20)
text_display.config(state=tk.DISABLED)

hear_button = tk.Button(root, text="Hear", command=on_hear_button_click)
hear_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(root, text="Stop", command=on_stop_button_click)
stop_button.pack(side=tk.LEFT, padx=10)

delete_button = tk.Button(root, text="Delete Old", command=on_delete_button_click)
delete_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
