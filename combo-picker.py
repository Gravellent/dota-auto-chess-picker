#!/usr/bin/env python

import ttk
from Tkinter import *
from csv import reader
from PIL import ImageTk,Image

_VERSION = "0.7"
_PIECES_FILE = "database/csv/pieces.csv"
_COMBOS_FILE = "database/csv/combos.csv"

_DEFAULT_COLOR = "#d9d9d9"
_AZURE_COLOR = "#5795f9"
_BLUE_COLOR = "#144593"
_GREEN_COLOR = "#66ce54"
_YELLOW_COLOR = "#f9ef31"
_PURPLE_COLOR = "#8757f9"
_RED_COLOR = "#ff4f4f"

PIECES = {}
COMBOS = {}

BUTTONS = []
WIDGETS = []

def load_pieces():
  global PIECES

  with open(_PIECES_FILE) as csv_file:
    csv_reader = reader(csv_file, delimiter=';')
    next(csv_file)

    for line in csv_reader:
     PIECES[line[0]] = [line[1], line[2], line[3]]

def load_combos():
  global COMBOS

  with open(_COMBOS_FILE) as csv_file:
    csv_reader = reader(csv_file, delimiter=';')
    next(csv_file)

    for line in csv_reader:
      if not line[1] in COMBOS.keys():
        COMBOS[line[1]] = []

      COMBOS[line[1]].append([line[0], line[2], line[3], line[4]])

def reset_all_buttons():
  global BUTTONS
  global _DEFAULT_COLOR

  for button in BUTTONS:
    button[1].config(bg = _DEFAULT_COLOR)

def highlight_piece(piece_name):
  global BUTTONS
  global _RED_COLOR

  for button in BUTTONS:
    if button[0] == piece_name:
      button[1].config(bg = _RED_COLOR)

def button_click(piece_name):
  reset_all_buttons()

  highlight_piece(piece_name)

def add_button(window, piece, level, column, row):
  button = Button(window)
  button.grid(column = column, row = row)

  img = ImageTk.PhotoImage(Image.open( \
                           "images/pieces/" + piece + ".png"))

  button.config(image = img, command = lambda:button_click(piece), \
                compound = TOP, text = '* ' * int(level), \
                font=("Arial Bold", 5), pady = 0, padx = 0)

  return [piece, button, img]

def sort_priority(val):
  return val[0]

def add_combos(window, game_phase):
  global BUTTONS
  global PIECES
  global COMBOS

  row = 0

  combos = COMBOS[game_phase]
  combos.sort(key = sort_priority)

  for combo in combos:
    label = Label(window, font=("Arial Bold", 12), text = combo[1])
    label.grid(column = 0, row = row)

    WIDGETS.append(label)

    pieces = [x.strip() for x in combo[3].split(',')]

    column = 1
    for piece in pieces:
        BUTTONS.append(add_button(window, piece, PIECES[piece][2], \
                                  column, row))
        column += 1

    row += 1

def make_window():
  global VERSION

  window = Tk()

  window.title("Dota Auto Chess Strategy Picker " + _VERSION)

  notebook = ttk.Notebook(window)

  earlygame_page = ttk.Frame(notebook)
  notebook.add(earlygame_page, text="Earlygame")
  add_combos(earlygame_page, "Earlygame")

  midgame_page = ttk.Frame(notebook)
  notebook.add(midgame_page, text="Midgame")
  add_combos(midgame_page, "Midgame")

  lategame_page = ttk.Frame(notebook)
  notebook.add(lategame_page, text="Lategame")
  add_combos(lategame_page, "Lategame")

  notebook.pack(expand=1, fill="both")

  window.bind('<Escape>', lambda event, a = True: reset_buttons(a))

  window.mainloop()

def main():
  load_pieces()

  load_combos()

  make_window()

if __name__ == '__main__':
  main()
