import os, glob
import pandas as pd
from datetime import date as dt

def test_merge():

    master_df = pd.DataFrame()
    dfs = []
    
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "./exports/vrbo_exports/*.csv"))
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
        
    master_df.to_csv(f"./uploads/VRBO_EXPORT_Test.csv", index=False)