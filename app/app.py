from tkinter import Tk
from tkinter import Frame
from tkinter.ttk import Style
from pages.HomePage import HomePage
from pages.DeckPage import DeckPage


class HSKFlashcardApp(Tk):
    def __init__(self):
        super().__init__()

        self.title("HSK Flashcard App")

        self.WIDTH, self.HEIGHT = 1100, 700
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.place_in_center_of_screen()

        self.bind("<Down>", lambda event: self.exit_app())

        self.option_add("*Font", ("Arial", 24))
        self.option_add("*background", "#1F2024")
        self.option_add("*foreground", "#83B5D1")
        self.style = Style()
        self.style.configure("TButton", font=("Arial", 16), background="#304250")

        self.container = Frame(self, padx=20, pady=20)
        self.container.pack(expand=True, fill="both")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.pages = {
            'HomePage': HomePage(self),
            'HSK1': DeckPage(self, deck='data/HSK1.json'),
            'HSK2': DeckPage(self, deck='data/HSK2.json'),
            'HSK3': DeckPage(self, deck='data/HSK3.json'),
            'HSK4': DeckPage(self, deck='data/HSK4.json'),
            'HSK5': DeckPage(self, deck='data/HSK5.json'),
            'HSK6': DeckPage(self, deck='data/HSK6.json'),
        }
        self.show_page(self.pages['HomePage'])

    def show_page(self, frame):
        self.current_page = frame
        self.current_page.grid(row=0, column=0, sticky='nesw')
        self.current_page.tkraise()
        self.current_page.focus_set()

    def place_in_center_of_screen(self):
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        place_coordinates = (int((screen_width - self.WIDTH)/2), int((screen_height - self.HEIGHT)/4))
        self.geometry(f"+{place_coordinates[0]}+{place_coordinates[1]}")

    def exit_app(self):
        for page in self.pages:
            if page != "HomePage":
                self.pages[page].save_deck()
        exit()


if __name__ == '__main__':
    app = HSKFlashcardApp()
    app.mainloop()