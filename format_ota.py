import re
import pandas as pd
from datetime import datetime, date as dt
from categories import ota_cat_dict as cat

def date_format(od):
    date_str = re.search(r"\d{2}/\d{2}/\d{4}", od)
    res = datetime.strptime(date_str.group(), "%d/%m/%Y").date()
    return (f"{res.strftime('%m/%d/%Y')}T01:00:00.000GMT")

def create_ota_unformatted(csv_files):
    master_df = pd.DataFrame()
    dfs = []

    for f in csv_files:
        # Finds the topic in row 8
        pc_item = pd.read_csv(f, nrows=8)
        pc = pc_item.iat[7, 0]
        # Pulls all data from line 14 onwards
        df = pd.read_csv(f, skiprows=13)
        new_data = pd.DataFrame(df)
        
        new_data["Topic"] = pc[38:]
        
        dfs.append(new_data)
    
    master_df = pd.concat(dfs)
    master_df.to_csv(f"./uploads/OTA_EXPORT_{dt.today()}.csv", index=False, encoding='utf-8-sig')
    
def create_ota_formatted(csv_files):
    master_df = pd.DataFrame()
    dfs = []
    
    for f in csv_files:
        pc_item = pd.read_csv(f, nrows=8)
        pc = pc_item.iat[7,0]
        df = pd.read_csv(f, skiprows=13)
        data = pd.DataFrame(df)
        
        data["Topic"] = pc[38:]
        data["Primary Category"] = [cat[topic] for topic in data["Topic"]]
        data["Description"] = data["Sentence"] + "\n----- \n" + data["Verbatim"]
        data["Case Origin"] = "Dataloader"
        data["Record Type ID"] = "Partner Review"
        data["Contact Name"] = "Internal Contacts"
        data["Case Category"] = "Guest Review"
        data["Type"] = ["Health & Safety Investigation Level 1" if cat == "Fire" or cat == "Balcony" or cat == "Gas" else "Health & Safety Investigation Level 3" if  cat == "Electrical" or  cat == "Pest-Control" or cat == "Beach Safety" or cat == "Transport" else "Health & Safety Investigation Level 2" for cat in data["Primary Category"]]
        data["Owner ID"] = ["005C0000003oGdn" if primCat == "Fire" or primCat == "Gas" else "0058b00000FdW4I" for primCat in data["Primary Category"]]
        data["Status"] = ["New" if primCat == "Fire" or primCat == "Gas" else "Pending - Vendor" for primCat in data["Primary Category"]]
        data["Blocker"] = ["" if primCat == "Fire" or primCat == "Gas" else "Awaiting Response" for primCat in data["Primary Category"]]
        data["Auto Chase Status"] = "Not Applicable"
        data["Translated Description"] = "NULL"
        
        #Push data to DFS list
        dfs.append(data)
        
    master_df = pd.concat(dfs)
    
    master_df["Document Date"] = [date_format(date) for date in master_df["Document Date"]]
    master_df["Sentence"] = [sentence[:250] for sentence in master_df["Sentence"]]
    
    master_df = master_df.rename(columns={
        "NaturalId": "Review ID",
        "Document Date": "Review Submission Date Time",
        "ADM_EXPEDIAHOTELID": "Account ID",
        "HR_TPID": "TPID",
        "Sentence": "Subject"
    })

    master_df = master_df[
        ["Review ID", "Review Submission Date Time", "Account ID", "TPID", "Subject", "Primary Category", "Description",
         "Case Origin",
         "Record Type ID",
         "Contact Name",
         "Owner ID",
         "Case Category",
         "Type",
         "Status",
         "Blocker",
         "Auto Chase Status",
         "Translated Description"]
    ]

    master_df = master_df.drop_duplicates(subset="Review ID", keep="first")
    
    # Final document to CSV
    master_df.to_csv(f"./uploads/OTA_UPLOAD_{dt.today()}.csv", index=False, encoding='utf-8-sig')
    
