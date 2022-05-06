from tkinter.ttk import Button
from tkinter import Label
from tkinter import Frame


class HomePage(Frame):
    def __init__(self, parent):
        super().__init__(parent.container)

        Label(self, text="HSK Flashcard App", font=("Arial", 72)).pack(expand=True)
        Label(self, text="Choose a deck to begin:").pack(expand=True)

        buttons_frame = Frame(self, background='green')
        buttons_frame.pack(expand=True)

        Button(buttons_frame, text="HSK1", command=lambda: parent.show_page(parent.pages['HSK1'])).grid(row=0, column=0, padx=5, pady=5)
        Button(buttons_frame, text="HSK2", command=lambda: parent.show_page(parent.pages['HSK2'])).grid(row=1, column=0, padx=5, pady=5)
        Button(buttons_frame, text="HSK3", command=lambda: parent.show_page(parent.pages['HSK3'])).grid(row=2, column=0, padx=5, pady=5)
        Button(buttons_frame, text="HSK4", command=lambda: parent.show_page(parent.pages['HSK4'])).grid(row=0, column=1, padx=5, pady=5)
        Button(buttons_frame, text="HSK5", command=lambda: parent.show_page(parent.pages['HSK5'])).grid(row=1, column=1, padx=5, pady=5)
        Button(buttons_frame, text="HSK6", command=lambda: parent.show_page(parent.pages['HSK6'])).grid(row=2, column=1, padx=5, pady=5)
        Button(buttons_frame, text="Load Deck").grid(row=0, column=2, padx=5, pady=5)
        Button(buttons_frame, text="Custom Select").grid(row=1, column=2, padx=5, pady=5)
        Button(buttons_frame, text="Starred Deck").grid(row=2, column=2, padx=5, pady=5)

