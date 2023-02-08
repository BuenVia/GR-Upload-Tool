import os, glob, re
import pandas as pd
from datetime import datetime, date as dt
from googletrans import Translator
from categories import cat_dict as cat

trans = Translator()

def date_format(od):
    date_str = re.search(r"\d{2}/\d{2}/\d{4}", od)
    res = datetime.strptime(date_str.group(), "%d/%m/%Y").date()
    return (f"{res.strftime('%m/%d/%Y')}T01:00:00.000GMT")

def test_merge():
    master_df = pd.DataFrame()
    dfs = []
    
    # Pull the data from each file
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "./exports/vrbo_exports/*.csv"))
    for f in csv_files:
        
        # Find string that contains topic name on line 8
        pc_item = pd.read_csv(f, nrows=8)
        pc = pc_item.iat[7,0]
        
        new_item = pd.read_csv(f, skiprows=13)
        data = pd.DataFrame(new_item)
        
        data["Topic"] = pc[35:]
        # Creates topic column in DF using the topic list above
        data["Primary Category"] = [cat[t]["primCat"] for t in data["Topic"]]
        data["Secondary Category"] = [cat[t]["secCat"] for t in data["Topic"]]
        # Creates a a new column called Description in the DF which is a merge of the Sentence, Review Title and Verbatim
        data["Description"] = "SENTENCE: \n" + data["Sentence"] + "\nTITLE: \n" + data["REVIEW_TITLE"] + "\nREVIEW: \n" +data["Verbatim"] + "\nBrand: VRBO"
        # Creates a new column for columns that don't exist from the export
        data["Validated Listing ID"] = data["ADM_EXPEDIAHOTELID"]
        data["Case Origin"] = "Dataloader"
        data["Record Type ID"] = "Partner Review"
        data["Contact Name"] = "Internal Contacts"
        data["Case Category"] = "Guest Review"
        # Work out the case type based on the data["Primary Category"]
        data["Type"] = ["Health & Safety Investigation Level 1" if cat == "Fire" or cat == "Balcon" or cat == "Gas" else "Health & Safety Investigation Level 3" if  cat == "Electrical" or  cat == "Pest-Control" or cat == "Beach Safety" or cat == "Transport" else "Health & Safety Investigation Level 2" for cat in data["Primary Category"]]
        data["Owner ID"] = ["005C0000003oGdn" if primCat == "Fire" or primCat == "Gas" else "0058b00000FdW4I" for primCat in data["Primary Category"]]
        data["Status"] = ["New" if primCat == "Fire" or primCat == "Gas" else "Pending - Vendor" for primCat in data["Primary Category"]]
        data["Blocker"] = ["" if primCat == "Fire" or primCat == "Gas" else "Awaiting Response" for primCat in data["Primary Category"]]
        data["Auto Chase Status"] = "Not Applicable"
        
        # tr = trans.translate("Hola, buenas tardes.")
        # print(tr.text)
               
        dfs.append(data)
    
    # Merge the data in to one file    
    master_df = pd.concat(dfs)
    
    # Format the columns
    master_df["Document Date"] = [date_format(date) for date in master_df["Document Date"]]
    master_df["Sentence"] = [sentence[:250] for sentence in master_df["Sentence"]]
    #TODO 1 - TRANSLATIONS
    master_df["Translated Description"] = "A"
    
    # Rename the columns
    master_df = master_df.rename(columns={
            "NaturalId": "Review ID",
            "Document Date": "Review Date Submission Time",
            "ADM_EXPEDIAHOTELID": "Account ID",
            "Sentence": "Subject"
        })
    
    # Change order of columns
    master_df = master_df[
        ["Review ID", 
         "Review Date Submission Time", 
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
    
    master_df.to_csv(f"./uploads/VRBO_UPLOAD_Test.csv", index=False, encoding='utf-8-sig')