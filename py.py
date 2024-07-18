import tkinter as tk
from tkinter import filedialog
import pyttsx3
import PyPDF4
import os

def select_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        create_ui(file_path)

def create_ui(pdf_file):
    root = tk.Tk()
    root.title("PDF to Audiobook Converter")

    # Add radio buttons for voice gender
    gender_var = tk.StringVar()
    male_radio = tk.Radiobutton(root, text="Male Voice", variable=gender_var, value="m")
    female_radio = tk.Radiobutton(root, text="Female Voice", variable=gender_var, value="f")
    male_radio.pack()
    female_radio.pack()

    # Add a slider for adjusting speech rate
    speed_label = tk.Label(root, text="Adjust Speech Rate:")
    speed_slider = tk.Scale(root, from_=50, to=200, orient="horizontal")
    speed_label.pack()
    speed_slider.pack()

    def convert_to_audio():
        gender = gender_var.get()
        speed = speed_slider.get() / 100.0  # Convert to a float between 0.5 and 2.0

        pdf_reader = PyPDF4.PdfFileReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extractText()

        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        if gender == "m":
            engine.setProperty("voice", voices[0].id)  # Male voice
        elif gender == "f":
            engine.setProperty("voice", voices[1].id)  # Female voice
        engine.setProperty("rate", speed)  # Set speech rate

        engine.save_to_file(text, "output.mp3")
        engine.runAndWait()

        os.system("start output.mp3")

    convert_button = tk.Button(root, text="Convert to Audiobook", command=convert_to_audio)
    convert_button.pack()

    root.mainloop()

if __name__ == "__main__":
    select_pdf_file()
