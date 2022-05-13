from datetime import datetime
import json
import platform
import random
from tkinter import Frame, Label
from tkinter.ttk import Button

FONTS = {
    'TitleFont': ("Arial", 42),
    'CardFont': ("Kaiti", 200) if "Windows" in platform.system() else ("Kaiti SC", 200),  # Calligraphy standard
    'DefaultFont': ("Arial", 24),
}
COLORS = {
    "DefaultBackground": "#32353B",
    "StarredText": "#f5cc00"
}


class DeckPage(Frame):
    def __init__(self, parent, deck):
        super().__init__(parent.container)

        self.bind("<Right>", lambda event: self.change_card(new_card_id=self.current_card_id+1))
        self.bind("<Left>", lambda event: self.change_card(new_card_id=self.current_card_id-1))
        self.bind("<Up>", lambda event: self.reveal_card())

        self.deck = deck

        with open(self.deck, 'r', encoding='utf8') as f:
            try:
                self.complete_deck_data = json.load(f)
            except json.decoder.JSONDecodeError:
                exit(f"{self.deck} is invalid! Check if it's a valid .JSON file.")

        self.deck_data = self.sort_deck(self.complete_deck_data)

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
        filters_frame = Frame(self)
        buttons_frame = Frame(self, pady=10)

        title_frame.grid(row=0, column=0)
        card_frame.grid(row=1, column=0, sticky='nesw')
        # Center widgets in card_frame
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_rowconfigure(0, weight=1)

        last_studied_frame.grid(row=2, column=0)
        filters_frame.grid(row=3, column=0)
        buttons_frame.grid(row=4, column=0)

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

        Button(filters_frame, text="Characters Only", command=lambda: self.filter_deck(tag="character")).grid(row=0, column=0, padx=5, pady=5)
        Button(filters_frame, text="Words Only", command=lambda: self.filter_deck(tag="word")).grid(row=0, column=1, padx=5, pady=5)
        Button(filters_frame, text="Starred Only", command=lambda: self.filter_deck(tag="Starred")).grid(row=0, column=2, padx=5, pady=5)
        Button(filters_frame, text="All Cards", command=lambda: self.filter_deck()).grid(row=0, column=3, padx=5, pady=5)

        Button(buttons_frame, text="Previous", command=lambda: self.change_card(new_card_id=self.current_card_id-1)).grid(row=0, column=0, padx=5, pady=5)
        Button(buttons_frame, text="Next", command=lambda: self.change_card(new_card_id=self.current_card_id+1)).grid(row=0, column=1, padx=5, pady=5)
        Button(buttons_frame, text="Reveal", command=self.reveal_card).grid(row=1, column=0, padx=5, pady=5)
        Button(buttons_frame, text="Star", command=self.star_card).grid(row=1, column=1, padx=5, pady=5)
        Button(buttons_frame, text="Home Page", command=lambda: parent.show_page(parent.pages['HomePage'])).grid(row=2, column=0, columnspan=2, pady=15)

    def render_card(self):
        # If deck is empty, display "No Cards!" and clear other widgets
        if not self.deck_data:
            self.title_label.configure(text='')
            self.card_label.configure(text="No Cards!")
            self.card_definition_label.configure(text='')
            self.last_studied_label.configure(text='')
            return

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

    def filter_deck(self, tag=None):
        # Filters the current deck based on the specified tag and re-renders
        # Deck is a dict

        # Merge the modified deck with the complete deck (i.e. update last studied dates) before filtering
        self.complete_deck_data |= self.deck_data

        if tag == 'Starred':
            deck_data = self.deck_data
            filtered_dict = {card: deck_data[card] for card in deck_data if deck_data[card]["Starred"]}
            self.deck_data = filtered_dict
        elif tag:
            deck_data = self.complete_deck_data
            filtered_dict = {card: deck_data[card] for card in deck_data if tag in deck_data[card]["Tags"]}
            self.deck_data = filtered_dict
        else:
            self.deck_data = self.complete_deck_data

        self.deck_data = self.sort_deck(self.deck_data)
        self.current_card_id = 0
        self.render_card()
        self.focus_set()

    def sort_deck(self, deck, sort_method="study_date"):
        if sort_method == "random":
            cards = list(deck.keys())
            random.shuffle(cards)
            sorted_deck = {card: deck[card].copy() for card in cards}

            return sorted_deck
        elif sort_method == "study_date":
            card_study_date_dict = {card: self.days_since_date(deck[card]["LastStudied"]) for card in deck}
            # Split deck into groups of the same last studied date (e.g. {"Never": [Card1, Card2], "10/05/2022": [Card4, Card5]})
            grouped_cards_by_study_date = {}
            for card in card_study_date_dict:
                date = card_study_date_dict[card]
                if date not in grouped_cards_by_study_date:
                    grouped_cards_by_study_date[date] = []
                grouped_cards_by_study_date[date].append(card)
            # Shuffle items in each group
            for group in grouped_cards_by_study_date:
                items = grouped_cards_by_study_date[group]
                random.shuffle(items)
                grouped_cards_by_study_date[group] = items
            # Sort the deck starting with never studied cards
            # Copy is used so that sorted_deck is not linked with input deck
            sorted_deck = {}
            if "Never" in grouped_cards_by_study_date:
                never_studied_cards = grouped_cards_by_study_date.pop("Never")
                sorted_deck |= {card: deck[card].copy() for card in never_studied_cards}
            sorted_groups = sorted(list(grouped_cards_by_study_date.keys()), reverse=True)
            for group in sorted_groups:
                sorted_deck |= {card: deck[card].copy() for card in grouped_cards_by_study_date[group]}

            return sorted_deck

    def change_card(self, new_card_id):
        if 0 <= new_card_id < len(self.deck_data):
            self.current_card_id = new_card_id
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
        # Merge the modified deck with the complete deck (i.e. update last studied dates)
        self.complete_deck_data |= self.deck_data
        with open(self.deck, "w", encoding="utf8") as f:
            json.dump(self.complete_deck_data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def days_since_date(date):
        if not date:  # If date is none (i.e. card never studied)
            return "Never"
        else:
            date = datetime.strptime(date, "%d/%m/%Y")
            return (datetime.today() - date).days
