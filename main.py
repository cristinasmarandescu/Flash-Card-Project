from tkinter import *
from random import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    # Get from data the remaining words to learn in French.
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    # If the file "words_to_learn" does not exist, get words from the "french_words" file and create a new dictionary.
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # Create a dictionary from data with words to learn.
    to_learn = data.to_dict(orient="records")


def next_card():
    """
    Gets the next card with a random French word after 3 seconds have passed.
    """
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    """
    Flips the card in order to see the English translation of the previous French word.
    """
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def is_known():
    """
    Removes the word from the dictionary of French words to be learned.
    Creates a new file with the words to learn.
    Gets the next card.
    """
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.cvs", index=False)
    next_card()


# Configure the tkinter window.
window = Tk()
window.title("Flash Card Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Set a timer for flipping cards.
flip_timer = window.after(3000, flip_card)

# Configure the tkinter canvas, cards and buttons.
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, font=("Arial", 40, "italic"), text="")
card_word = canvas.create_text(400, 280, font=("Arial", 60, "bold"), text="")
canvas.grid(column=0, row=0, columnspan=2)

right_button_img = PhotoImage(file="./images/right.png")
known_button = Button(image=right_button_img, highlightthickness=0, bd=0, command=is_known)
known_button.grid(column=1, row=1)

wrong_button_img = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=wrong_button_img, highlightthickness=0, bd=0, command=next_card)
unknown_button.grid(column=0, row=1)

next_card()


window.mainloop()