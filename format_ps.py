import re
import pandas as pd
from datetime import datetime, date as dt

def date_format(od):
    date_str = re.search(r"\d{2}/\d{2}/\d{4}", od)
    res = datetime.strptime(date_str.group(), "%d/%m/%Y").date()
    return (f"{res.strftime('%m/%d/%Y')}T01:00:00.000GMT")

def create_ps_unformatted(csv_files):
    master_df = pd.DataFrame()
    dfs = []
    
    for f in csv_files:
        pc_item = pd.read_csv(f, nrows=8)
        pc = pc_item.iat[7, 0]
        
        df = pd.read_csv(f, skiprows=38)
        new_data = pd.DataFrame(df)
        
        new_data["Topic"] = pc[40:]
        
        dfs.append(new_data)
        
    master_df = pd.concat(dfs)
    master_df.to_csv(f"./uploads/PS_EXPORT_{dt.today()}.csv", index=False, encoding='utf-8-sig')
    
def create_ps_formatted(csv_files):
    master_df = pd.DataFrame()
    dfs = []
    
    for f in csv_files:
        pc_item = pd.read_csv(f, nrows=8)
        pc = pc_item.iat[7, 0]
        df = pd.read_csv(f, skiprows=38)
        data = pd.DataFrame(df)
        
        data["Topic"] = pc[40:]
        data["Primary Category"] = "Customer"
        data["Secondary Category"] = [secCat for secCat in data["Topic"]]
        data["Description"] = data["Sentence"] + "\n----- \n" + data["Verbatim"]
        data["Owner ID"] = "0058b00000FGSZI"
        data["Record Type ID"] = "Partner Review"
        data["Type"] = "Health & Safety Personal Safety"
        data["Status"] = ["Closed" if secCat == "Drug Activity-Other" or secCat == "Theft" else "Pending - Internal" for secCat in data["Secondary Category"]]
        data["Blocker"] = ["" if secCat == "Drug Activity-Other" or secCat == "Theft" else "Awaiting Internal Team" for secCat in data["Secondary Category"]]
        data["Resolution Type"] = ["Not Processed" if secCat == "Drug Activity-Other" or secCat == "Theft" else "" for secCat in data["Secondary Category"]]
        data["Resolution Outcome"] = ["No investigation required" if secCat == "Drug Activity-Other" or secCat == "" else "Awaiting Internal Team" for secCat in data["Secondary Category"]]
        data["Contact Name"] = "Internal Contacts"
        data["Case Category"] = "Guest Review"
        data["Case Origin"] = "Dataloader"
        data["Translated Description"] = ""
        
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
        [
            "Review ID", "Review Submission Date Time", "Account ID", "TPID", 
            "Primary Category", "Secondary Category", "Subject", "Description",
            "Owner ID", "Record Type ID", "Type", "Status", "Blocker","Resolution Type", 
            "Resolution Outcome", "Contact Name", "Case Category", "Case Origin", "Translated Description"
        ]
    ]
    
    master_df = master_df.drop_duplicates(subset="Review ID", keep="first")
    
    # Final document to CSV
    master_df.to_csv(f"./uploads/PS_UPLOAD_{dt.today()}.csv", index=False, encoding='utf-8-sig')