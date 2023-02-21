import re
import pandas as pd
from datetime import datetime, date as dt
from categories import ota_cat_dict as ota_cat, cat_dict as cat

def date_format(od):
    if re.search(r"\d{2}/\d{2}/\d{4}", od) == None:
        date_str = re.search(r"\d{1}/\d{2}/\d{2}", od)
        res = datetime.strptime(date_str.group(), "%x").date()
    else:
        date_str = re.search(r"\d{2}/\d{2}/\d{4}", od)
        res = datetime.strptime(date_str.group(), "%d/%m/%Y").date()
    return (f"{res.strftime('%m/%d/%Y')}T01:00:00.000GMT")

def create_unformatted(csv_files, brand):
    master_df = pd.DataFrame()
    dfs = []

    for f in csv_files:
        # Finds the topic in row 8
        pc_item = pd.read_csv(f, nrows=8)
        pc = pc_item.iat[7, 0]
        # Pulls all data from header row - row is different for each brand
        if brand == "ota" or brand == "vrbo":
            df = pd.read_csv(f, skiprows=13)
        elif brand == "ps":
            df = pd.read_csv(f, skiprows=38)
        new_data = pd.DataFrame(df)
        
        if brand == "ota":
            new_data["Topic"] = pc[38:]
        elif brand == "vrbo":
            new_data["Topic"] = pc[35:]
        elif brand == "ps":
            new_data["Topic"] = pc[40:]

        dfs.append(new_data)
    
    master_df = pd.concat(dfs)
    master_df.to_csv(f"./uploads/{brand}_EXPORT_{dt.today()}.csv", index=False, encoding='utf-8-sig')
    
def create_formatted(csv_files, brand):
    master_df = pd.DataFrame()
    dfs = []
    
    for f in csv_files:
        # Finds the topic in row 8
        pc_item = pd.read_csv(f, nrows=8)
        pc = pc_item.iat[7, 0]
        # Pulls all data from header row - row is different for each brand
        if brand == "ota" or brand == "vrbo":
            df = pd.read_csv(f, skiprows=13)
        elif brand == "ps":
            df = pd.read_csv(f, skiprows=38)
        data = pd.DataFrame(df)
        
        data["Case Origin"] = "Dataloader"
        data["Record Type ID"] = "Partner Review"
        data["Contact Name"] = "Internal Contacts"
        data["Case Category"] = "Guest Review"
        data["Translated Description"] = "NULL"
        data["Auto Chase Status"] = "Not Applicable"
        if brand == "vrbo":
            data["Topic"] = pc[35:]
            data["Primary Category"] = [cat[t]["primCat"] for t in data["Topic"]]
            data["Secondary Category"] = [cat[t]["secCat"] for t in data["Topic"]]
            data["Type"] = ["Health & Safety Investigation Level 1" if cat == "Fire" or cat == "Balcony" or cat == "Gas" else "Health & Safety Investigation Level 3" if  cat == "Electrical" or  cat == "Pest-Control" or cat == "Beach Safety" or cat == "Transport" else "Health & Safety Investigation Level 2" for cat in data["Primary Category"]]
            data["Owner ID"] = ["005C0000003oGdn" if primCat == "Fire" or primCat == "Gas" else "0058b00000FdW4I" for primCat in data["Primary Category"]]
            data["Status"] = ["New" if primCat == "Fire" or primCat == "Gas" else "Pending - Vendor" for primCat in data["Primary Category"]]
            data["Blocker"] = ["" if primCat == "Fire" or primCat == "Gas" else "Awaiting Response" for primCat in data["Primary Category"]]
            data["Validated Listing ID"] = data["ADM_EXPEDIAHOTELID"]
            data["Description"] = data["Sentence"] + "\n----\n" + data["REVIEW_TITLE"] + "\n----\n" +data["Verbatim"] + "\nBrand: VRBO"
        elif brand == "ota":
            data["Topic"] = pc[38:]
            data["Primary Category"] = [ota_cat[topic] for topic in data["Topic"]]
            data["Description"] = data["Sentence"] + "\n----- \n" + data["Verbatim"]
            data["Type"] = ["Health & Safety Investigation Level 1" if cat == "Fire" or cat == "Balcony" or cat == "Gas" else "Health & Safety Investigation Level 3" if  cat == "Electrical" or  cat == "Pest-Control" or cat == "Beach Safety" or cat == "Transport" else "Health & Safety Investigation Level 2" for cat in data["Primary Category"]]
            data["Owner ID"] = ["005C0000003oGdn" if primCat == "Fire" or primCat == "Gas" else "0058b00000FdW4I" for primCat in data["Primary Category"]]
            data["Status"] = ["New" if primCat == "Fire" or primCat == "Gas" else "Pending - Vendor" for primCat in data["Primary Category"]]
            data["Blocker"] = ["" if primCat == "Fire" or primCat == "Gas" else "Awaiting Response" for primCat in data["Primary Category"]]
        elif brand == "ps":
            data["Topic"] = pc[40:]
            data["Primary Category"] = "Customer"
            data["Secondary Category"] = [secCat for secCat in data["Topic"]]
            data["Description"] = data["Sentence"] + "\n----- \n" + data["Verbatim"]
            data["Owner ID"] = "0058b00000FGSZI"
            data["Type"] = "Health & Safety Personal Safety"
            data["Status"] = ["Closed" if secCat == "Drug Activity-Other" or secCat == "Theft" else "Pending - Internal" for secCat in data["Secondary Category"]]
            data["Blocker"] = ["" if secCat == "Drug Activity-Other" or secCat == "Theft" else "Awaiting Internal Team" for secCat in data["Secondary Category"]]
            data["Resolution Type"] = ["Not Processed" if secCat == "Drug Activity-Other" or secCat == "Theft" else "" for secCat in data["Secondary Category"]]
            data["Resolution Outcome"] = ["No investigation required" if secCat == "Drug Activity-Other" or secCat == "" else "Awaiting Internal Team" for secCat in data["Secondary Category"]]
        
        dfs.append(data)
    
    master_df = pd.concat(dfs)
    
    master_df["Document Date"] = [date_format(date) for date in master_df["Document Date"]]
    master_df["Sentence"] = [sentence[:250] for sentence in master_df["Sentence"]]
    
    if brand == "vrbo":
        master_df = master_df.rename(columns={
            "NaturalId": "Review ID",
            "Document Date": "Review Submission Date Time",
            "ADM_EXPEDIAHOTELID": "Account ID",
            "Sentence": "Subject"
        })
    elif brand == "ota" or brand == "ps":
        master_df = master_df.rename(columns={
            "NaturalId": "Review ID",
            "Document Date": "Review Submission Date Time",
            "ADM_EXPEDIAHOTELID": "Account ID",
            "HR_TPID": "TPID",
            "Sentence": "Subject"
        })
        
    if brand == "vrbo":
        master_df = master_df[
            ["Review ID", 
            "Review Submission Date Time", 
            "Account ID",
            "Validated Listing ID",
            "Subject",
            "Primary Category",
            "Secondary Category",
            "Description",
            "Case Origin",
            "Record Type ID",
            "Contact Name",
            "Owner ID",
            "Case Category",
            "Type",
            "Status",
            "Blocker",
            "Auto Chase Status",
            "Translated Description"
            ]
        ]
    elif brand == "ota":
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
    elif brand == "ps":
        master_df = master_df[
            [
                "Review ID", "Review Submission Date Time", "Account ID", "TPID", 
                "Primary Category", "Secondary Category", "Subject", "Description",
                "Owner ID", "Record Type ID", "Type", "Status", "Blocker","Resolution Type", 
                "Resolution Outcome", "Contact Name", "Case Category", "Case Origin", "Translated Description"
            ]
        ]
            
    # Sort list by case type
    master_df = master_df.sort_values(by=['Type'])
    # Drop duplicates
    master_df = master_df.drop_duplicates(subset="Review ID", keep="first")
    # Final document to CSV
    master_df.to_csv(f"./uploads/{brand}_UPLOAD_{dt.today()}.csv", index=False, encoding='utf-8-sig')
    