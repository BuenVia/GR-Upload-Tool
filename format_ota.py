import os, glob
import pandas as pd


path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "./exports/ota_exports/*.csv"))
dfs = []

for f in csv_files:
    df = pd.read_csv(f, header=22)
#     new_data = pd.DataFrame(df)
#     dfs.append(new_data)
     
# master_df = pd.concat(dfs)
# master_df.to_csv('TEST_FILE.csv', index=False)
