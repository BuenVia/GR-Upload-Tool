from tkinter import messagebox
import os, glob
import pandas as pd
from datetime import date as dt

def create_vrbo_unformatted():

    master_df = pd.DataFrame()
    dfs = []
    
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "./exports/vrbo_exports/*.csv"))
    
    if len(csv_files) == 0:
        messagebox.showinfo(title="Error", message="No files found in the './exports/vrbo_exports' directory.")
    else:
        for f in csv_files:
            pc_item = pd.read_csv(f, nrows=8)
            pc = pc_item.iat[7,0]
            
            x = pd.read_csv(f, skiprows=13)
            new_data = pd.DataFrame(x)
            
            topic = []
            for _ in range(len(new_data)):
                topic.append(pc[35:])
                
            new_data["Topic"] = topic
            
            dfs.append(new_data)
            
        master_df = pd.concat(dfs)
            
        master_df.to_csv(f"./uploads/VRBO_EXPORT_{dt.today()}.csv", index=False)