import time, pandas as pd
from datetime import datetime, date
from categories import ota_cat_dict as ota_cat, cat_dict as vrbo_cat #, ps_cat_dict as ps_cat, tpid_codes

class FormatCsv:
    
    def __init__(self, review_list, model, start_date):
        self.review_list = review_list
        if len(self.review_list) > 0:
            self.raw_data_to_csv(model)
            self.format_csv(model, start_date)
        else:
            print("Nothing to return")

    def raw_data_to_csv(self, model):
        master_df = pd.DataFrame(self.review_list)
        master_df.to_csv(f"./uploads/raw_{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
        
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
        
        if model == "H&S VRBO Model - REF":
            data["Validated Listing ID"] = data["adm_expediahotelid"]
            data["Primary Category"] = [vrbo_cat[primCat]["primCat"] for primCat in data["topic"]]
            data["Secondary Category"] = [vrbo_cat[primCat]["secCat"] for primCat in data["topic"]]
            data["Type"] = ["Health & Safety Investigation Level 1" if cat == "Fire" or cat == "Balcony/Deck/Porch" or cat == "Gas" or cat == "Customer L1" else "Health & Safety Investigation Level 3" if  cat == "Electrical" or  cat == "Pest-Control" or cat == "Beach Safety" or cat == "Transport" else "Health & Safety Investigation Level 2" for cat in data["Primary Category"]]
            data["Owner ID"] = ["0058b00000FdW4I" if primCat == "Balcony" else "005C0000003oGdn" for primCat in data["Primary Category"]]
            data["Status"] = ["Pending - Vendor" if primCat == "Balcony" else "New" for primCat in data["Primary Category"]]
            data["Blocker"] = ["Awaiting Response" if primCat == "Balcony" else "" for primCat in data["Primary Category"]]
            data["Description"] = data["_words"] + "\n----\n" + data["review_title"] + "\n----\n" + data["verbatim"] + "\nBrand: VRBO"
        
        if model == "Health and Safety - Ref":
            data["Primary Category"] = [ota_cat[topic] for topic in data["topic"]]
            data["Description"] = data["_words"] + "\n----\n" + data["verbatim"]
            data["Type"] = ["Health & Safety Investigation Level 1" if cat == "Fire" or cat == "Balcony/Deck/Porch" or cat == "Gas" or cat == "Customer L1" else "Health & Safety Investigation Level 3" if  cat == "Electrical" or  cat == "Pest-Control" or cat == "Beach Safety" or cat == "Transport" else "Health & Safety Investigation Level 2" for cat in data["Primary Category"]]
            data["Owner ID"] = ["0058b00000FdW4I" if primCat == "Balcony" else "005C0000003oGdn" for primCat in data["Primary Category"]]            
            data["Status"] = ["Pending - Vendor" if primCat == "Balcony" else "New" for primCat in data["Primary Category"]]
            data["Blocker"] = ["Awaiting Response" if primCat == "Balcony" else "" for primCat in data["Primary Category"]]
            
            #TODO Build out closing chains.
            # Work out the logic for closing chains
            # data["Status"] = ["Closed" if chain == "wyndham hotels & resorts" else data["Status"] for chain in data["ha_parentchainname"]]
            # for chain in data["ha_parentchainname"]:
            #     if chain == "wyndham hotels & resorts":
            #         data["Status"] == "Closed"
   
        # if model == "H&S Personal Safety - Ref":                
        #     data["Primary Category"] = [ps_cat[topic] for topic in data["topic"]]
        #     data["Description"] = data["_words"] + "\n----\n" + data["verbatim"]
        #     data["Type"] = ["Health & Safety Investigation Level 1" if cat == "Customer L1" else "Health & Safety Investigation Level 2" if  cat == "Customer L2" else "Health & Safety Investigation Level 3" for cat in data["Primary Category"]]
        #     data["Owner ID"] = "005C0000003oGdn"
        #     data["Status"] = "New"
        #     data["Blocker"] = ""
        #     data["Language"] = "English"

            
        # if model == "LX H&S - Ref":
        #     data["Activity H&S"] = [topic for topic in data["topic"]]
        #     data["Description"] = data["_words"] + "\n----\n" + data["verbatim"]
        #     data["Primary Category"] = [topic.split(" - ")[1] for topic in data["topic"]]
        #     data["Secondary Category"] = [topic.split(" - ")[0] for topic in data["topic"]]
        #     data["Team"] = "Health and Safety"
        #     data["Status"] = ["Closed" if item == "33574" or item == "28065" else "New" for item in data["hr_supplier_id"]]
        #     data["Owner ID"] = "0054W00000Ee7kLQAR"
        #     data["Case Record Type"] = "LX Health & Safety"
        #     data["hr_tpid"] = [tpid_codes[code] 
        #                        if code == "de_de" 
        #                        or code == "en_au" 
        #                        or code == "en_ca" 
        #                        or code == "en_gb" 
        #                        or code == "en_ie" 
        #                        or code == "en_us" 
        #                        or code == "es_co" 
        #                        or code == "es_es" 
        #                        or code == "es_mx" 
        #                        or code == "es_us" 
        #                        or code == "fr_ca" 
        #                        or code == "fr_fr" 
        #                        or code == "it_it" 
        #                        or code == "ja_jp" 
        #                        or code == "ko_kr" 
        #                        or code == "nl_nl" 
        #                        or code == "pt_br" 
        #                        or code == "pt_pt" 
        #                        or code == "sv_se" 
        #                        or code == "tr_tr" 
        #                        or code == "zh_hk" 
        #                        or code == "zh_tw" 
        #                        else "0" for code in data["hr_display_locale"]]
        #     data["Type"] = ["Health & Safety Investigation Level 1" 
        #                     if primCat =="Air Accident" 
        #                     or primCat =="Pilot error" 
        #                     or primCat == "Fire Alarm Incident" 
        #                     or primCat == "Fire alarm not working/faulty/missing" 
        #                     or primCat == "Fire call points not in use" 
        #                     or primCat == "Fire exits obstructed or locked" 
        #                     or primCat == "Fire in venue" 
        #                     or primCat == "Inadequate means of escape" 
        #                     else "Health & Safety Investigation Level 2" for primCat in data["Primary Category"]]
        #     data["Business Hours ID"] = "01mE0000000Xl0P"
                    
        # Organise column order
        if model == "H&S VRBO Model - REF":
            # Change column names
            data = data.rename(columns={
                "review_id": "Review ID",
                "adm_expediahotelid": "Account ID",
                "_doc_time": "Review Submission Date Time"
            })
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
            data = data.sort_values(by=["Type"])
            data = data.drop_duplicates(subset="Review ID", keep="first")
            data.to_csv(f"./uploads/UPLOAD_{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
            
            fatality_data = data[ (data["Secondary Category"] == "Fatality") ]
            fatality_data.to_csv(f"./uploads/FATALITY{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
        
        if model == "Health and Safety - Ref":
            # Change column names
            data = data.rename(columns={
                "review_id": "Review ID",
                "adm_expediahotelid": "Account ID",
                "_doc_time": "Review Submission Date Time",
                "hr_tpid": "TPID"
            })
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
                "Translated Description",
                # "Test"
            ]]            
            data = data.sort_values(by=["Type"])
            data = data.drop_duplicates(subset="Review ID", keep="first")
            data.to_csv(f"./uploads/UPLOAD_{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
            
            fatality_data = data[ (data["Primary Category"] == "Fatality") ]
            fatality_data.to_csv(f"./uploads/FATALITY{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
        
        # if model == "H&S Personal Safety - Ref":
        #     # Change column names
        #     data = data.rename(columns={
        #         "review_id": "Review ID",
        #         "adm_expediahotelid": "Account ID",
        #         "_doc_time": "Review Submission Date Time",
        #         "hr_tpid": "TPID",
        #     })
        #     data = data[
        #         [
        #             "Review ID", "Review Submission Date Time", "Account ID", "TPID", 
        #             "Primary Category", "Subject", "Description",
        #             "Owner ID", "Record Type ID", "Type", "Status", "Blocker",
        #             "Contact ID", "Case Category", "Case Origin", "Language"
        #         ]
        #     ]
        #     # Removes category 'Drugs Smell' from the final sheet.
        #     # data = data[data["Secondary Category"] != "Drugs Smell"]
        #     data = data.sort_values(by=["Type"])
        #     data = data.drop_duplicates(subset="Review ID", keep="first")
        #     data.to_csv(f"./uploads/UPLOAD_{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
        
        # if model == "LX H&S - Ref":
        #     # Change column names
        #     data = data.rename(columns={
        #         "natural_id": "Review ID",
        #         "_doc_time": "Review Submission Date Time",
        #         "hr_tpid": "TPID",
        #         "hr_product_name": "Activity Name",
        #         "hr_supplier_branch_id": "Account Branch ID",
        #         "hr_supplier_id": "Account ID for 3P"
        #     })
        #     # Order columns
        #     data = data[
        #         [
        #             "Review ID", "Review Submission Date Time", "Activity H&S", "Activity Name", 
        #             "Account Branch ID", "Account ID for 3P", "TPID", "Subject", "Description", 
        #             "Primary Category", "Type", "Case Category", "Secondary Category", "Team", "Case Origin",
        #             "Status", "Owner ID", "Case Record Type", "Business Hours ID"
        #         ]
        #     ]
            
        #     data_third_party = data[ (data["Account ID for 3P"] == "33574") | (data["Account ID for 3P"] == "28065")]
        #     data_third_party = data_third_party.sort_values(by=["Type"])
        #     data_third_party = data_third_party.drop_duplicates(subset="Review ID", keep="first")
        #     data_third_party.to_csv(f"./uploads/3P_UPLOAD_{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
            
        #     data_non = data[ (data["Account ID for 3P"] != "33574") & (data["Account ID for 3P"] != "28065")]
        #     data_non = data_non.sort_values(by=["Type"])
        #     data_non = data_non.drop_duplicates(subset="Review ID", keep="first")
        #     data_non.to_csv(f"./uploads/NON3P_UPLOAD_{model}_{date.today()}_{time.time()}.csv", encoding='utf-8-sig', index=False)
