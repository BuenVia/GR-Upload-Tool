import pandas as pd
import os, glob, re
from datetime import date as dt

# Dictionary with list for each column in export csv
def create_unformatted():
    result_dict = {
        "Review ID": [],
        "Sentence ID": [],
        "Source": [],
        "ADM_EXPEDIAHOTELID": [],
        "CB Date of Creation": [],
        "Document Date": [],
        "HA_HOTELNAME": [],
        "HR_DISPLAYLOCALE": [],
        "HR_TSPID": [],
        "REVIEW_TITLE": [],
        "Sentence": [],
        "VerbatimType": [],
        "Verbatim": [],
        "Topic": []
    }

    # get the files
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    # For each file, extract all information from row 14 onwards
    for f in csv_files:

        # Searches for the topic name in the 9th row
        pc_item = pd.read_csv(f, nrows=8)
        pc = pc_item.iat[7,0]

        new_item = pd.read_csv(f, skiprows=13)
        data = pd.DataFrame(new_item)
        # Push each column to relevant list in dictionary
        for natural in data.NaturalId:
            result_dict["Review ID"].append(natural)
        for sentence in data.SentenceId:
            result_dict["Sentence ID"].append(sentence)
        for source in data.Source:
            result_dict["Source"].append(source)
        for adm in data.ADM_EXPEDIAHOTELID:
            result_dict["ADM_EXPEDIAHOTELID"].append(adm)
        for cb in data["CB Date of Creation"]:
            result_dict["CB Date of Creation"].append(cb)
        for date in data["Document Date"]:
            result_dict["Document Date"].append(date)
        for hotel_name in data["HA_HOTELNAME"]:
            result_dict["HA_HOTELNAME"].append(hotel_name)
        for display_locale in data["HR_DISPLAYLOCALE"]:
            result_dict["HR_DISPLAYLOCALE"].append(display_locale)
        for tspid in data["HR_TSPID"]:
            result_dict["HR_TSPID"].append(tspid)
        for title in data["REVIEW_TITLE"]:
            result_dict["REVIEW_TITLE"].append(title)
        for sent in data["Sentence"]:
            result_dict["Sentence"].append(sent)
        for verbatim_type in data["VerbatimType"]:
            result_dict["VerbatimType"].append(verbatim_type)
        for verbatim in data["Verbatim"]:
            result_dict["Verbatim"].append(verbatim)
        # Appends topic name to Topic key in dictionary for number of times NaturalId appears. Slices first 3 chars.
        for natural in data.NaturalId:
            result_dict["Topic"].append(pc[35:])

    # Create a dataframe from the final dictionary and create CSV
    df = pd.DataFrame(result_dict)
    # df.to_csv(f"EXPORT_VRBO_{datetime.now().strftime('%M_%S')}.csv")
    df.to_csv(f"../EXPORT_VRBO_{dt.today()}.csv")