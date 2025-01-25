import customtkinter as ctk
from tkinter import Text, Scrollbar, filedialog, messagebox, END
from googletrans import Translator
import pyttsx3
import speech_recognition as sr

# Functions
def translate_text():
    input_text = input_box.get("1.0", END).strip()
    source_lang = src_lang_entry.get().strip()
    target_lang = target_lang_entry.get().strip()

    if not input_text or not target_lang:
        output_box.delete("1.0", END)
        output_box.insert(END, "Please provide text and target language.")
        return

    try:
        translator = Translator()
        if not source_lang:
            detected_lang = translator.detect(input_text)
            source_lang = detected_lang.lang

        translation = translator.translate(input_text, src=source_lang, dest=target_lang)
        output_box.delete("1.0", END)
        output_box.insert(END, f"Detected Source Language: {source_lang}\nTranslated Text:\n{translation.text}")
    except Exception as e:
        output_box.delete("1.0", END)
        output_box.insert(END, f"Error: {str(e)}")

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            input_box.delete("1.0", END)
            input_box.insert(END, content)

def save_translation():
    translated_text = output_box.get("1.0", END).strip()
    if not translated_text:
        messagebox.showwarning("Warning", "No translated text to save!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(translated_text)
        messagebox.showinfo("Success", "Translation saved successfully!")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            output_box.delete("1.0", END)
            output_box.insert(END, "Listening... Speak now!")
            audio = recognizer.listen(source, timeout=5)
            input_text = recognizer.recognize_google(audio)
            input_box.delete("1.0", END)
            input_box.insert(END, input_text)
        except sr.UnknownValueError:
            output_box.delete("1.0", END)
            output_box.insert(END, "Sorry, I could not understand your speech.")
        except Exception as e:
            output_box.delete("1.0", END)
            output_box.insert(END, f"Error: {str(e)}")

def text_to_speech():
    translated_text = output_box.get("1.0", END).strip()
    if not translated_text:
        messagebox.showwarning("Warning", "No text to convert to speech!")
        return

    try:
        engine = pyttsx3.init()
        engine.say(translated_text)
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", f"Speech synthesis failed: {str(e)}")

# Initialize CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Advanced Language Translator")
app.geometry("800x600")

# UI Components
ctk.CTkLabel(app, text="Source Language (e.g., 'en'):").pack(pady=5)
src_lang_entry = ctk.CTkEntry(app, width=200)
src_lang_entry.pack(pady=5)

ctk.CTkLabel(app, text="Target Language (e.g., 'fr'):").pack(pady=5)
target_lang_entry = ctk.CTkEntry(app, width=200)
target_lang_entry.pack(pady=5)

ctk.CTkLabel(app, text="Input Text:").pack(pady=5)
input_box = Text(app, height=8, width=70)
input_box.pack(pady=5)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="Translate", command=translate_text).grid(row=0, column=0, padx=10)
ctk.CTkButton(button_frame, text="Upload File", command=upload_file).grid(row=0, column=1, padx=10)
ctk.CTkButton(button_frame, text="Save Translation", command=save_translation).grid(row=0, column=2, padx=10)
ctk.CTkButton(button_frame, text="Speech to Text", command=speech_to_text).grid(row=0, column=3, padx=10)
ctk.CTkButton(button_frame, text="Text to Speech", command=text_to_speech).grid(row=0, column=4, padx=10)

ctk.CTkLabel(app, text="Translated Text:").pack(pady=5)
output_box = Text(app, height=8, width=70)
output_box.pack(pady=5)

app.mainloop()
