from tkinter import *
from tkinter import messagebox
import os, glob
from vrbo_formatter import create_vrbo_formatted, create_vrbo_unformatted


"""
First part of the program returns the unformatted csv with the raw data extracted from SalesForce.
Second part of the program formats the data ready for DataLoader.
"""

def vrbo_format():
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "./exports/vrbo_exports/*.csv"))
    
    if len(csv_files) == 0:
        messagebox.showinfo(title="Error", message="No files found in the './exports/vrbo_exports' directory.")
    else:
        create_vrbo_unformatted(csv_files)
        create_vrbo_formatted(csv_files)

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