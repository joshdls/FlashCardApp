import tkinter
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
FOREIGN_LANGUAGE_FONT = ("Ariel", 40, "italic")
ENGLISH_LANGUAGE_FONT = ("Ariel", 60, "bold")
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv", index=False)
    next_card()


window = tkinter.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = tkinter.Canvas(width=800, height=526)
card_front_img = tkinter.PhotoImage(file="./images/card_front.png")
card_back_img = tkinter.PhotoImage(file="./images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_img)

card_title = canvas.create_text(400, 150, text="", font=FOREIGN_LANGUAGE_FONT)
card_word = canvas.create_text(400, 263, text="", font=ENGLISH_LANGUAGE_FONT)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

cross_image = tkinter.PhotoImage(file="./images/wrong.png")
unknown_button = tkinter.Button(image=cross_image, command=next_card)
unknown_button.grid(column=0, row=1)

check_image = tkinter.PhotoImage(file="./images/right.png")
check_button = tkinter.Button(image=check_image, command=is_known)
check_button.grid(column=1, row=1)

next_card()


window.mainloop()





