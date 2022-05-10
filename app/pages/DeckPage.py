from datetime import datetime
import json
from tkinter.ttk import Button
from tkinter import Frame, Label
from pprint import pprint

FONTS = {
    'TitleFont': ("Arial", 42),
    'CardFont': ("Kaiti SC", 200),  # Calligraphy standard
    'DefaultFont': ("Arial", 24),
}
COLORS = {
    "DefaultBackground": "#32353B",
    "StarredText": "#f5cc00"
}

class DeckPage(Frame):
    def __init__(self, parent, deck):
        super().__init__(parent.container)

        self.bind("<Right>", lambda event: self.next_card())
        self.bind("<Left>", lambda event: self.prev_card())
        self.bind("<Up>", lambda event: self.reveal_card())

        self.deck = deck
        self.tags = ["character", "word"]

        with open(self.deck, 'r', encoding='utf8') as f:
            self.raw_deck_data = json.load(f)

        self.deck_data = self.sort_deck(self.raw_deck_data)

        # Center widgets horizontally
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.current_card_id = 0
        self.current_card = list(self.deck_data.keys())[self.current_card_id]
        self.card_last_studied_date = self.deck_data[self.current_card]["LastStudied"]

        title_frame = Frame(self)
        card_frame = Frame(self, padx=10, pady=10, background=COLORS["DefaultBackground"], highlightthickness=1, highlightbackground='white')
        last_studied_frame = Frame(self)
        buttons_frame = Frame(self, pady=10)

        title_frame.grid(row=0, column=0)
        card_frame.grid(row=1, column=0, sticky='nesw')
        # Center widgets in card_frame
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_rowconfigure(0, weight=1)

        last_studied_frame.grid(row=2, column=0)
        buttons_frame.grid(row=3, column=0)

        # Create card widgets and initialize to nothing
        self.title_label = Label(title_frame, font=FONTS['TitleFont'])
        self.title_label.pack()

        self.card_definition_label = Label(card_frame, background=COLORS['DefaultBackground'], foreground="#DDA15E", wraplength=1050)
        self.card_definition_label.grid(row=0, column=0)

        self.card_label = Label(card_frame, font=FONTS['CardFont'], background=COLORS['DefaultBackground'])
        self.card_label.grid(row=1, column=0)

        self.last_studied_label = Label(last_studied_frame)
        self.last_studied_label.pack()

        self.render_card()  # initialize first card

        Button(buttons_frame, text="Previous", command=self.prev_card).grid(row=0, column=0, padx=5, pady=5)
        Button(buttons_frame, text="Next", command=self.next_card).grid(row=0, column=1, padx=5, pady=5)
        Button(buttons_frame, text="Reveal", command=self.reveal_card).grid(row=1, column=0, padx=5, pady=5)
        Button(buttons_frame, text="Star", command=self.star_card).grid(row=1, column=1, padx=5, pady=5)
        Button(buttons_frame, text="Home Page", command=lambda: parent.show_page(parent.pages['HomePage'])).grid(row=2, column=0, columnspan=2, pady=15)

    def render_card(self):
        # Update card data
        self.current_card = list(self.deck_data.keys())[self.current_card_id]
        self.card_last_studied_date = self.deck_data[self.current_card]["LastStudied"]

        # Render card title, text, and hide definition
        self.title_label.configure(text=f'{self.current_card_id+1}/{len(self.deck_data)}')
        self.card_definition_label.configure(text='')
        self.card_label.configure(text=self.current_card)

        # Change card background if starred
        if self.deck_data[self.current_card]["Starred"]:
            self.card_label.configure(foreground=COLORS["StarredText"])
        else:
            self.card_label.configure(foreground="#83B5D1")

        # Render the card's last studied date
        if self.card_last_studied_date:
            last_studied_string = f"Last Studied: {self.card_last_studied_date} ({self.days_since_date(self.card_last_studied_date)} days ago)"
        else:
            last_studied_string = 'Last Studied: Never'
        self.last_studied_label.configure(text=last_studied_string)

        # Update last studied date to today
        self.deck_data[self.current_card]["LastStudied"] = datetime.today().strftime("%d/%m/%Y")

    def filter_deck(self, deck, tag):
        # Filters the deck based on the specified tag
        # Deck is a dict
        filtered_dict = {card: deck[card] for card in deck if tag in deck[card]["Tags"]}

        return filtered_dict

    def sort_deck(self, deck):
        deck_dict = {}
        for card in deck:
            deck_dict[card] = self.days_since_date(deck[card]["LastStudied"])
        sorted_deck = {k: deck[k]  for k, v in sorted(deck_dict.items(), key=lambda item: item[1], reverse=True)}

        return sorted_deck

    def next_card(self):
        if (self.current_card_id + 1) < len(self.deck_data):
            self.current_card_id += 1
            self.render_card()
        self.focus_set()

    def prev_card(self):
        if (self.current_card_id - 1) >= 0:
            self.current_card_id -= 1
            self.render_card()
        self.focus_set()

    def reveal_card(self):
        self.card_definition_label.configure(text=self.deck_data[self.current_card]['Definition'])
        self.focus_set()  # Focus on current widget so keyboard binds work

    def star_card(self):
        self.deck_data[self.current_card]["Starred"] = not self.deck_data[self.current_card]["Starred"]
        self.render_card()
        self.focus_set()

    def save_deck(self):
        # Merge the modified deck with the raw deck.
        to_save_deck = self.raw_deck_data | self.deck_data
        with open(self.deck, "w") as f:
            json.dump(to_save_deck, f, ensure_ascii=False, indent=2)

    @staticmethod
    def days_since_date(date):
        try:
            date = datetime.strptime(date, "%d/%m/%Y")
            return (datetime.today() - date).days
        except TypeError:
            return -1
