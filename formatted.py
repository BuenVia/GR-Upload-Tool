import pandas as pd
import os, glob, re
from datetime import date as dt
from datetime import datetime

#TODO 1. Format the data during the process

def create_formatted():
    formatted_dict = {
        "Review ID": [],
        "Review Submission Date Time": [],
        "Account ID": [],
        "Validated Listing ID": [],
        "Subject": [],
        "Primary Category": [],
        "Secondary Category": [],
        "Description": [],
        "Case Origin": [],
        "Record Type ID": [],
        "Contact Name": [],
        "Owner ID": [],
        "Case Category": [],
        "Type": [],
        "Status": [],
        "Blocker": [],
        "Auto Chase Status": [],
        "Translated Description": []
    }

    # get the files
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    # For each file, extract all information from row 14 onwards
    for f in csv_files:

        pc_item = pd.read_csv(f, nrows=8)
        pc = pc_item.iat[7,0]

        new_item = pd.read_csv(f, skiprows=13)
        data = pd.DataFrame(new_item)

        # Merges the Sentence, REVIEW_TITLE and Verbatim columns together to create a description column
        data["Description"] = "SENTENCE: \n" + data["Sentence"] + "\nTITLE: \n" + data["REVIEW_TITLE"] + "\nREVIEW: \n" +data["Verbatim"] + "\nBrand: VRBO"
        data["Translated Description"] = data["Sentence"] + "--------" + data["Verbatim"]

        # Push each column to relevant list in dictionary
        for natural in data["NaturalId"]:
            formatted_dict["Review ID"].append(natural)
        # Format the datetime so that it is suitable for Dataloader
        for date in data["Document Date"]:
            date_str = re.search(r"\d{2}/\d{2}/\d{4}", date)
            res = datetime.strptime(date_str.group(), "%d/%m/%Y").date()
            x = (f"{res.strftime('%x')}T01:00:00.000GMT")
            formatted_dict["Review Submission Date Time"].append(x)
        for adm in data["ADM_EXPEDIAHOTELID"]:
            formatted_dict["Account ID"].append(adm)
            formatted_dict["Validated Listing ID"].append(adm)
        for sent in data["Sentence"]:
            formatted_dict["Subject"].append(sent[0:250])
        for natural in data["NaturalId"]:
            if pc[35:] == "Electrical - Power Outage":
                formatted_dict["Primary Category"].append("Electrical")
                formatted_dict["Secondary Category"].append("Power Outage")
            elif pc[35:] == "Electrical - Faulty Equipment":
                formatted_dict["Primary Category"].append("Electrical")
                formatted_dict["Secondary Category"].append("Faulty Equipment")
            elif pc[35:] == "Electrical - Loose or exposed wiring":
                formatted_dict["Primary Category"].append("Electrical")
                formatted_dict["Secondary Category"].append("Loose or exposed wiring")
            elif pc[35:] == "Electrical - Electric Shocks":
                formatted_dict["Primary Category"].append("Electrical")
                formatted_dict["Secondary Category"].append("Electric Shocks")
            elif pc[35:] == "Electrical - Broken Sockets":
                formatted_dict["Primary Category"].append("Electrical")
                formatted_dict["Secondary Category"].append("Broken Sockets")
            elif pc[35:] == "Accommodation - Bathroom Safety":
                formatted_dict["Primary Category"].append("Accommodation")
                formatted_dict["Secondary Category"].append("Bathroom Safety")
            elif pc[35:] == "Accommodation - Slippery Surfaces":
                formatted_dict["Primary Category"].append("Accommodation")
                formatted_dict["Secondary Category"].append("Slippery Surfaces")
            elif pc[35:] == "Pool Chlorinated Water":
                formatted_dict["Primary Category"].append("Pool Safety")
                formatted_dict["Secondary Category"].append("Excessive Chlorine")
            elif pc[35:] == "Pool Unclean Water":
                formatted_dict["Primary Category"].append("Pool Safety")
                formatted_dict["Secondary Category"].append("Unclean / Cloudy Pool Water")
            elif pc[35:] == "Pest-Control - Bed Bugs":
                formatted_dict["Primary Category"].append("Pest-Control")
                formatted_dict["Secondary Category"].append("Bed Bugs")
            elif pc[35:] == "Pest-Control - Mice":
                formatted_dict["Primary Category"].append("Pest-Control")
                formatted_dict["Secondary Category"].append("Rats/Mice")
            elif pc[35:] == "Pest-Control - Cockroaches":
                formatted_dict["Primary Category"].append("Pest-Control")
                formatted_dict["Secondary Category"].append("Cockroaches")
            elif pc[35:] == "Pest-Control - Use of pesticide":
                formatted_dict["Primary Category"].append("Pest-Control")
                formatted_dict["Secondary Category"].append("Use of pesticide")
            elif pc[35:] == "Stairs":
                formatted_dict["Primary Category"].append("Stairway")
                formatted_dict["Secondary Category"].append("")
            elif pc[35:] == "Transport/Excursions":
                formatted_dict["Primary Category"].append("Transport")
                formatted_dict["Secondary Category"].append("")
            else:
                formatted_dict["Primary Category"].append(pc[35:])
                formatted_dict["Secondary Category"].append("")
        for description in data["Description"]:
            formatted_dict["Description"].append(description)
        for n in data["NaturalId"]:
            formatted_dict["Case Origin"].append("Dataloader")
        for n in data["NaturalId"]:
            formatted_dict["Record Type ID"].append("Partner Review")
        for n in data["NaturalId"]:
            formatted_dict["Contact Name"].append("internal contacts")
        #Logic for working out owner ID
        for n in data["NaturalId"]:
            if pc[35:] == "Fire" or pc[35:] == "Gas":
                formatted_dict["Owner ID"].append("005C0000003oGdn")
            else:
                formatted_dict["Owner ID"].append("0058b00000FdW4I")
        for n in data["NaturalId"]:
            formatted_dict["Case Category"].append("Guest Review")
        #Logic for working out the case type
        for n in data["NaturalId"]:
            if pc[35:] == "Fire" or pc[35:] == "Balcony" or pc[35:] == "Gas":
                formatted_dict["Type"].append("Health & Safety Investigation Level 1")
            elif pc[35:] == "Electrical - Power Outage" or pc[35:] == "Electrical - Faulty Equipment" or pc[35:] == "Electrical - Loose or exposed wiring" or pc[35:] == "Electrical - Electric Shocks" or pc[35:] == "Electrical - Broken Sockets":
                formatted_dict["Type"].append("Health & Safety Investigation Level 3")
            elif pc[35:] == "Transport/Excursions" or pc[35:] == "Beach Safety":
                formatted_dict["Type"].append("Health & Safety Investigation Level 3")
            elif pc[35:] == "Pest-Control - Bed Bugs" or pc[35:] == "Pest-Control - Mice" or pc[35:] == "Pest-Control - Cockroaches" or pc[35:] == "Pest-Control - Use of pesticide":
                formatted_dict["Type"].append("Health & Safety Investigation Level 3")
            else:
                formatted_dict["Type"].append("Health & Safety Investigation Level 2")
        #Logic for working out the status
        for n in data["NaturalId"]:
            if pc[35:] == "Fire" or pc[35:] == "Balcony" or pc[35:] == "Gas":
                formatted_dict["Status"].append("New")
            else:
                formatted_dict["Status"].append("Pending - Internal")
        #Logic for working out the blocker
        for n in data["NaturalId"]:
            if pc[35:] == "Fire" or pc[35:] == "Balcony" or pc[35:] == "Gas":
                formatted_dict["Blocker"].append("")
            else:
                formatted_dict["Blocker"].append("Awaiting Internal Team")
        for n in data["NaturalId"]:
            formatted_dict["Auto Chase Status"].append("Not Applicable")
        #TODO 2. Logic for working out the translated description
        for trans_desc in data["Translated Description"]:
            formatted_dict["Translated Description"].append("NULL")

    mf = pd.DataFrame(formatted_dict)
    # mf.to_csv(f"formatted_{datetime.now().strftime('%M_%S')}.csv", index=False, encoding='utf-8-sig')
    mf.to_csv(f"../UPLOAD_VRBO_{dt.today()}.csv", index=False, encoding='utf-8-sig')
