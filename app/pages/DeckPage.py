from datetime import datetime
import json
from tkinter.ttk import Button
from tkinter import Frame, Label
from pprint import pprint

FONTS = {
    'TitleFont': ("Arial", 42),
    'CardFont': ("Arial", 200),
    'DefaultFont': ("Arial", 24),
}


class DeckPage(Frame):
    def __init__(self, parent, deck):
        super().__init__(parent.container)

        with open(deck, 'r', encoding='utf8') as f:
            self.deck_data = json.load(f)

        self.deck_data = self.sort_deck()

        self.current_card_id = 0
        self.current_card = list(self.deck_data.keys())[self.current_card_id]
        self.card_last_studied_date = self.deck_data[self.current_card]["LastStudied"]

        title_frame = Frame(self)
        card_frame = Frame(self, width=500, height=500, padx=10, pady=10, background="#32353B",
                           highlightthickness=1, highlightbackground='white')
        # card_frame.pack_propagate(False)
        last_studied_frame = Frame(self)
        buttons_frame = Frame(self, pady=10)

        title_frame.pack()
        card_frame.pack(fill="both", expand=True)
        last_studied_frame.pack()
        buttons_frame.pack(expand=True)

        self.title_label = Label(title_frame, text=f'Card {self.current_card_id+1}/{len(self.deck_data)}',
                                 font=FONTS['TitleFont'])
        self.title_label.pack(side='top')

        self.card_label = Label(card_frame, text=self.current_card, font=FONTS['CardFont'], background="#32353B",)
        self.card_label.pack(expand=True, fill="both")

        self.card_definition_label = Label(card_frame, text='', background="#32353B",)
        self.card_definition_label.pack(side="bottom", fill="x")

        self.last_studied_label = Label(last_studied_frame,
                                        text=f"Last Studied: {self.card_last_studied_date} "
                                             f"({self.days_since_date(self.card_last_studied_date)} days ago)")
        self.last_studied_label.pack(side="top")

        Button(buttons_frame, text="Previous", command=self.prev_card).grid(row=0, column=0, padx=5, pady=5)
        Button(buttons_frame, text="Next", command=self.next_card).grid(row=0, column=1, padx=5, pady=5)
        Button(buttons_frame, text="Reveal", command=self.reveal_card).grid(row=1, column=0, padx=5, pady=5)
        Button(buttons_frame, text="Star").grid(row=1, column=1, padx=5, pady=5)
        Button(buttons_frame, text="Home Page", command=lambda: parent.show_page(parent.pages['HomePage'])).grid(row=2, column=0, columnspan=2, pady=10)
        self.bind("<Right>", lambda event: self.next_card())
        self.bind("<Left>", lambda event: self.prev_card())

    def change_card(self):
        self.title_label.configure(text=f'Card {self.current_card_id+1}/{len(self.deck_data)}')
        self.card_definition_label.configure(text='')

        self.current_card = list(self.deck_data.keys())[self.current_card_id]
        self.card_label.configure(text=self.current_card)

        self.card_last_studied_date = self.deck_data[self.current_card]["LastStudied"]
        if self.card_last_studied_date:
            last_studied_string = f"Last Studied: {self.card_last_studied_date} ({self.days_since_date(self.card_last_studied_date)} days ago)"
        else:
            last_studied_string = 'Last Studied: Never'
        self.last_studied_label.configure(text=last_studied_string)

    def next_card(self):
        if (self.current_card_id + 1) < len(self.deck_data):
            self.current_card_id += 1
            self.change_card()

    def prev_card(self):
        if (self.current_card_id - 1) >= 0:
            self.current_card_id -= 1
            self.change_card()

    def reveal_card(self):
        self.card_definition_label.configure(text=f"{self.deck_data[self.current_card]['Definition']}")

    def sort_deck(self):
        deck_dict = {}
        for card in self.deck_data:
            deck_dict[card] = self.days_since_date(self.deck_data[card]["LastStudied"])
        sorted_deck = {k: self.deck_data[k]  for k, v in sorted(deck_dict.items(), key=lambda item: item[1], reverse=True)}

        return sorted_deck

    @staticmethod
    def days_since_date(date):
        try:
            date = datetime.strptime(date, "%d/%m/%Y")
            return (datetime.today() - date).days
        except TypeError:
            return -1


class Card(Frame):
    def __init__(self, parent_container, card):
        '''Card Object: {"card1": {"definition"...}}'''
        super().__init__(parent_container)
        self.card_text = card
        self.card_definition = card['Definition']
        self.card_last_studied = card["LastStudied"]

        self.card_frame = Frame(self)
        self.last_studied_frame = Frame(self)

        self.card_label = Label(self.card_frame, text=self.card_text)
        self.card_label.pack(side="top")

        self.card_definition_label = Label(self.card_frame, text='')
        self.card_definition_label.pack(side="top")

        self.last_studied_label = Label(self.last_studied_frame, text="Last Studied: 12/06/2022 (100 days ago)")
        self.last_studied_label.pack(side="top")
