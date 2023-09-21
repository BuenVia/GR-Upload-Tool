import time, pandas as pd
from datetime import datetime, date
from categories import ota_cat_dict as ota_cat, cat_dict as vrbo_cat #, ps_cat_dict as ps_cat, tpid_codes

# Class that formats the data returned from review_finder.py and returns various CSV files.
class FormatCsv:
    
    def __init__(self, review_list, model, start_date):
        self.review_list = review_list
        if len(self.review_list) > 0:
            self.raw_data_to_csv(model)
            self.format_csv(model, start_date)
        else:
            print("Nothing to return")

    # Dumps all the returned data to it's own CSV file without any manipulation
    def raw_data_to_csv(self, model):
        master_df = pd.DataFrame(self.review_list)
        master_df.to_csv(f"./uploads/raw_{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
        
    # Manipulates the data inline with SalesForce mapping requirements
    def format_csv(self, model, start_date):
        # Common attributes across all projects
        data = pd.DataFrame(self.review_list)    
        data["Subject"] = [subject[:250] for subject in data["_words"]]
        data["topic"] = [topic.split(">> ")[1] for topic in data["topic"]]
        data["Case Origin"] = "Dataloader"
        data["Record Type ID"] = "Partner Review"
        data["Contact ID"] = "003C0000018VDiDIAW"
        data["Case Category"] = "Guest Review"
        data["Auto Chase Status"] = "Not Applicable"
        data["Translated Description"] = "NULL"
        
        # VRBO model specific attributes
        if model == "H&S VRBO Model - REF":
            data["Validated Listing ID"] = data["adm_expediahotelid"]
            data["Primary Category"] = [vrbo_cat[primCat]["primCat"] for primCat in data["topic"]]
            data["Secondary Category"] = [vrbo_cat[primCat]["secCat"] for primCat in data["topic"]]
            data["Type"] = ["Health & Safety Investigation Level 1" if cat == "Fire" or cat == "Balcony/Deck/Porch" or cat == "Gas" or cat == "Customer L1" else "Health & Safety Investigation Level 3" if  cat == "Electrical" or  cat == "Pest-Control" or cat == "Beach Safety" or cat == "Transport" else "Health & Safety Investigation Level 2" for cat in data["Primary Category"]]
            data["Owner ID"] = ["0058b00000FdW4I" if primCat == "Balcony" else "005C0000003oGdn" for primCat in data["Primary Category"]]
            data["Status"] = ["Pending - Vendor" if primCat == "Balcony" else "New" for primCat in data["Primary Category"]]
            data["Blocker"] = ["Awaiting Response" if primCat == "Balcony" else "" for primCat in data["Primary Category"]]
            data["Description"] = data["_words"] + "\n----\n" + data["review_title"] + "\n----\n" + data["verbatim"] + "\nBrand: VRBO"
        
        # Core OTA specific attributes
        if model == "Health and Safety - Ref":
            data["Primary Category"] = [ota_cat[topic] for topic in data["topic"]]
            data["Description"] = data["_words"] + "\n----\n" + data["verbatim"]
            data["Type"] = ["Health & Safety Investigation Level 1" if cat == "Fire" or cat == "Balcony/Deck/Porch" or cat == "Gas" or cat == "Customer L1" else "Health & Safety Investigation Level 3" if  cat == "Electrical" or  cat == "Pest-Control" or cat == "Beach Safety" or cat == "Transport" else "Health & Safety Investigation Level 2" for cat in data["Primary Category"]]
            data["Owner ID"] = ["0058b00000FdW4I" if primCat == "Balcony" else "005C0000003oGdn" for primCat in data["Primary Category"]]            
            data["Status"] = ["Pending - Vendor" if primCat == "Balcony" else "New" for primCat in data["Primary Category"]]
            data["Blocker"] = ["Awaiting Response" if primCat == "Balcony" else "" for primCat in data["Primary Category"]]
                                           
        if model == "H&S VRBO Model - REF":
            # Change column names in line with SF mapping requirements
            data = data.rename(columns={
                "review_id": "Review ID",
                "adm_expediahotelid": "Account ID",
                "_doc_time": "Review Submission Date Time"
            })
            # Organise column order
            data = data[[
                "Review ID",
                "Review Submission Date Time",
                "Account ID",
                "Validated Listing ID",
                "Subject",
                "Primary Category",
                "Secondary Category",
                "Description",
                "Case Origin",
                "Record Type ID",
                "Contact ID",
                "Owner ID",
                "Case Category",
                "Type",
                "Status",
                "Blocker",
                "Auto Chase Status",
                "Translated Description"
            ]]
            # Returns CSV with data mapped for upload   
            data = data.sort_values(by=["Type"])
            data = data.drop_duplicates(subset="Review ID", keep="first")
            data.to_csv(f"./uploads/UPLOAD_{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
            # Separates out any data that contains fatality categories
            fatality_data = data[ (data["Secondary Category"] == "Fatality") ]
            fatality_data.to_csv(f"./uploads/FATALITY{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
        
        if model == "Health and Safety - Ref":
            # Change column names in line with SF mapping requirements
            data = data.rename(columns={
                "review_id": "Review ID",
                "adm_expediahotelid": "Account ID",
                "_doc_time": "Review Submission Date Time",
                "hr_tpid": "TPID"
            })
            # Organise column order
            data = data[[
                "Review ID",
                "Review Submission Date Time",
                "Account ID",
                "TPID",
                "Subject",
                "Primary Category",
                "Description",
                "Case Origin",
                "Record Type ID",
                "Contact ID",
                "Owner ID",
                "Case Category",
                "Type",
                "Status",
                "Blocker",
                "Auto Chase Status",
                "Translated Description"
            ]]      
            # Returns CSV with data mapped for upload      
            data = data.sort_values(by=["Type"])
            data = data.drop_duplicates(subset="Review ID", keep="first")
            data.to_csv(f"./uploads/UPLOAD_{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
            # Separates out any data that contains fatality categories
            fatality_data = data[ (data["Primary Category"] == "Fatality") ]
            fatality_data.to_csv(f"./uploads/FATALITY{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
        