from tkinter import *
from test import test_merge
from unformatted import create_vrbo_unformatted
from formatted import create_vrbo_formatted

"""
First part of the program returns the unformatted csv with the raw data extracted from SalesForce.
Second part of the program formats the data ready for DataLoader.
"""

def vrbo_format():
    # create_vrbo_formatted()
    # create_vrbo_unformatted()
    test_merge()

window = Tk()
window.minsize(800, 80)
window.title("Upload Tool")
window.config(padx=50, pady=50, bg="#48C9B0")

title_label = Label(text="CIGR Formatter", font=("Courier", 24, "bold"), fg="white", bg="#48C9B0", highlightthickness=0)
title_label.grid(column=1, row=0)

vrbo_format_btn = Button()
vrbo_format_btn.config(text="VRBO - Create Formatted Document...", command=vrbo_format, bg="#A2D9CE")
vrbo_format_btn.grid(column=0, row=1, padx=30, pady=30)




window.mainloop()