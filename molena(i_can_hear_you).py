import tkinter as tk
from tkinter import messagebox, ttk
import speech_recognition as sr
import pyttsx3
import threading
import os

r = sr.Recognizer()
engine = pyttsx3.init()

listening = False
listen_thread = None

LANGUAGES = {
    "English": "en-US",
    "Arabic": "ar-SA"
}

def hear_and_display(language_code):
    global listening
    while listening:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
                my_txt = r.recognize_google(audio, language=language_code)
                if my_txt:
                    display_and_write(my_txt)
                    speak_text(my_txt)
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
        except Exception as e:
            print(str(e))
        if not listening:
            break

def display_and_write(text):
    text_display.config(state=tk.NORMAL)
    text_display.insert(tk.END, text + "\n")
    text_display.config(state=tk.DISABLED)
    with open("My_Words.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def on_hear_button_click():
    global listening, listen_thread
    if not listening:
        listening = True
        selected_lang = language_var.get()
        language_code = LANGUAGES[selected_lang]
        listen_thread = threading.Thread(target=hear_and_display, args=(language_code,), daemon=True)
        listen_thread.start()

def on_stop_button_click():
    global listening
    listening = False
    print("Stopped listening to the microphone")

def on_delete_button_click():
    try:
        with open("My_Words.txt", "w", encoding="utf-8") as f:
            f.write("")
        messagebox.showinfo("Success", "Old words deleted successfully!")
        text_display.config(state=tk.NORMAL)
        text_display.delete("1.0", tk.END)
        text_display.config(state=tk.DISABLED)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")

root = tk.Tk()
root.title("Enhanced Speech Recognition")

text_display = tk.Text(root, height=12, width=60)
text_display.pack(pady=18)
text_display.config(state=tk.DISABLED)

control_frame = tk.Frame(root)
control_frame.pack(pady=8)

hear_button = tk.Button(control_frame, text="Hear", command=on_hear_button_click)
hear_button.pack(side=tk.LEFT, padx=9)

stop_button = tk.Button(control_frame, text="Stop", command=on_stop_button_click)
stop_button.pack(side=tk.LEFT, padx=9)

delete_button = tk.Button(control_frame, text="Delete Old", command=on_delete_button_click)
delete_button.pack(side=tk.LEFT, padx=9)

language_var = tk.StringVar(value="English")
lang_menu = ttk.Combobox(control_frame, textvariable=language_var, values=list(LANGUAGES.keys()), width=9, state="readonly")
lang_menu.pack(side=tk.LEFT, padx=9)

root.mainloop()
