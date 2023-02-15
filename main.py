from tkinter import *
from tkinter import messagebox, filedialog
import os, glob

from format_func import create_unformatted, create_formatted

"""
First part of the program returns the unformatted csv with the raw data extracted from SalesForce.
Second part of the program formats the data ready for DataLoader.
"""

def open_vrbo_files():
    csv_files = filedialog.askopenfilenames()
    create_unformatted(csv_files, "vrbo")
    create_formatted(csv_files, "vrbo")  
    show_files()

def open_ota_format():
    csv_files = filedialog.askopenfilenames()
    create_unformatted(csv_files, "ota")
    create_formatted(csv_files, "ota")
    show_files()
    
def open_ps_format():
    csv_files = filedialog.askopenfilenames()
    create_unformatted(csv_files, "ps")
    create_formatted(csv_files, "ps")
    show_files()

def delete_file():
    try:
        is_delete = messagebox.askokcancel(title="Delete", message="You are about to delete all formatted files.")
        if is_delete:   
            path = os.getcwd()
            csv_files = glob.glob(os.path.join(path, "./uploads/*.csv"))
            if len(csv_files) < 1:
                messagebox.showinfo(title="Empty", message="The folder is empty.")
                return
            else:
                for f in csv_files:
                    os.remove(f)
    except PermissionError as err:
        messagebox.showerror(title="Error", message=f"{err}\n\nPLEASE CLOSE THE SPREADHSEET THEN TRY AGAIN...")
    else:
        messagebox.showinfo(title="Success", message="Successfully deleted.")
        
def show_files():
    path = "./uploads/"
    path = os.path.realpath(path)
    os.startfile(path)

window = Tk()
window.minsize(80, 80)
window.title("Upload Tool")
window.config(padx=50, pady=50, bg="#48C9B0")

title_label = Label(text="CIGR Formatter", font=("Courier", 24, "bold"), fg="white", bg="#48C9B0", highlightthickness=0)
title_label.grid(column=0, row=0)

vrbo_format_btn = Button()
vrbo_format_btn.config(text="VRBO", command=open_vrbo_files, bg="#A2D9CE", padx=10, pady=10)
vrbo_format_btn.grid(column=0, row=1, padx=30, pady=30)

ota_format_btn = Button()
ota_format_btn.config(text="OTA", command=open_ota_format, bg="#A2D9CE", padx=10, pady=10)
ota_format_btn.grid(column=0, row=2, padx=30, pady=30)

ps_format_btn = Button()
ps_format_btn.config(text="Personal Safety", command=open_ps_format, bg="#A2D9CE", padx=10, pady=10)
ps_format_btn.grid(column=0, row=3, padx=30, pady=30)

delete_label = Label(text="Delete's all previously formatted files.", font=("Arial", 12, "normal"), fg="white", bg="#A2D9CE")
delete_label.grid(column=0, row=5)

delete_btn = Button()
delete_btn.config(text="DELETE", command=delete_file, bg="Red")
delete_btn.grid(column=0, row=6, padx=30, pady=10)

open_directory_btn = Button()
open_directory_btn.config(text="Show Files", command=show_files, bg="#A2D9CE")
open_directory_btn.grid(column=0, row=4, padx=30, pady=30)

# TODO Build out Core OTA
# TODO Select files
# TODO Delete button for the Upload files + export files
# TODO Build out Personal Safety
# ======
# TODO Build out Activities
# TODO Dupe Check
# TODO Translation funciontality
# TODO Error message(s)


window.mainloop()