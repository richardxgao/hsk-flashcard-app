from tkinter.ttk import Button, Style
from tkinter import Label
from tkinter import Frame


class HomePage(Frame):
    def __init__(self, parent):
        super().__init__(parent.container)

        Label(self, text="HSK Flashcard App", font=("Arial", 72)).pack(expand=True)

        self.style = Style()
        self.style.configure("TButton", font=("Arial", 20), background="blue")

        buttons_frame = Frame(self)
        buttons_frame.pack()

        Label(buttons_frame, text="Choose a deck to begin:").grid(row=0, column=0, columnspan=2)
        Button(buttons_frame, text="HSK1", command=lambda: parent.show_page(parent.pages['HSK1']),
               style="TButton").grid(row=1, column=0, padx=5, pady=5)
        Button(buttons_frame, text="HSK2", command=lambda: parent.show_page(parent.pages['HSK2'])).grid(row=2, column=0, padx=5, pady=5)
        Button(buttons_frame, text="HSK3", command=lambda: parent.show_page(parent.pages['HSK3'])).grid(row=3, column=0, padx=5, pady=5)
        Button(buttons_frame, text="HSK4", command=lambda: parent.show_page(parent.pages['HSK4'])).grid(row=1, column=1, padx=5, pady=5)
        Button(buttons_frame, text="HSK5", command=lambda: parent.show_page(parent.pages['HSK5'])).grid(row=2, column=1, padx=5, pady=5)
        Button(buttons_frame, text="HSK6", command=lambda: parent.show_page(parent.pages['HSK6'])).grid(row=3   , column=1, padx=5, pady=5)
        Button(buttons_frame, text="Load Deck").grid(row=4, column=0, padx=5, pady=5, columnspan=2)

