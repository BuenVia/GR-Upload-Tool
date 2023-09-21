from tkinter import *
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import os
import babel.numbers

from review_finder import ReviewFinder

review_finder = ReviewFinder()

# From date formatting function
def get_from_date(date_str):
    x = datetime.strptime(date_str.get(), "%d/%m/%Y")
    unix = round(datetime.timestamp(x) * 1000)
    return unix

# To date formatting function (adds on 86399 seconds to return time of 23:59:59)
def get_to_date(date_str):
    x = datetime.strptime(date_str.get(), "%d/%m/%Y")
    end_of_day = datetime.timestamp(x) + 86399
    unix = round(end_of_day * 1000) 
    return str(unix)

def core_ota():
    fr = get_from_date(from_date)
    to = get_to_date(to_date)
    review_finder.call_sentences("Health and Safety - Ref", fr, to, info_label)

def vrbo():
    fr = get_from_date(from_date)
    to = get_to_date(to_date)
    review_finder.call_sentences("H&S VRBO Model - REF", fr, to, info_label)

def show_files():
    path = "./uploads/"
    path = os.path.realpath(path)
    os.startfile(path)
        
# GUI
window = Tk()
window.title("Guest Review Export and Upload")
window.config(padx=50, pady=50, bg="#ddd")

title_label = Label(text="Guest Review Export and Upload", font=("Courier", 24, "bold"), fg="#999", highlightthickness=0)
title_label.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

step_one_label = Label(text="1. Choose Date Range", font=("Courier", 18, "bold"))
step_one_label.grid(column=0, row=1)

from_label = Label(text="From")
from_label.grid(column=0, row=2, padx=10, pady=10)

to_label = Label(text="To")
to_label.grid(column=1, row=2, padx=10, pady=10)

from_date = DateEntry(locale="en_GB")
from_date.grid(column=0, row=3, padx=10, pady=10)

to_date = DateEntry(locale="en_GB")
to_date.grid(column=1, row=3, padx=10, pady=10)

step_two_label = Label(text="2. Choose Project", font=("Courier", 18, "bold"))
step_two_label.grid(column=0, row=4)

core_ota_btn = Button(text="Core OTA", command=core_ota)
core_ota_btn.grid(column=0, row=5, padx=10, pady=10)

vrbo_btn = Button(text="VRBO", command=vrbo)
vrbo_btn.grid(column=1, row=5, padx=10, pady=10)

info_label = Label()
info_label.grid(column=0, row=7)

open_directory_btn = Button()
open_directory_btn.config(text="Directory", command=show_files, bg="#A2D9CE")
open_directory_btn.grid(column=0, row=8, padx=30, pady=30)


window.mainloop()
