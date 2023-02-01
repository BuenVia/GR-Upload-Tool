import pandas as pd
import os
import glob
import re
from datetime import datetime

# # Dictionary with list for each column in export csv
# result_dict = {
#     "Natural ID": [],
#     "Sentence ID": [],
#     "Source": [],
#     "ADM_EXPEDIAHOTELID": [],
#     "CB Date of Creation": [],
#     "Document Date": [],
#     "HA_HOTELNAME": [],
#     "HR_DISPLAYLOCALE": [],
#     "HR_TSPID": [],
#     "REVIEW_TITLE": [],
#     "Sentence": [],
#     "VerbatimType": [],
#     "Verbatim": []
# }
#
# # get the files
# path = os.getcwd()
# csv_files = glob.glob(os.path.join(path, "*.csv"))
#
# # For each file, extract all information from row 14 onwards
# for f in csv_files:
#     new_item = pd.read_csv(f, skiprows=13)
#     data = pd.DataFrame(new_item)
#     # Push each column to relevant list in dictionary
#     for natural in data.NaturalId:
#         result_dict["Natural ID"].append(natural)
#     for sentence in data.SentenceId:
#         result_dict["Sentence ID"].append(sentence)
#     for source in data.Source:
#         result_dict["Source"].append(source)
#     for adm in data.ADM_EXPEDIAHOTELID:
#         result_dict["ADM_EXPEDIAHOTELID"].append(adm)
#     for cb in data["CB Date of Creation"]:
#         result_dict["CB Date of Creation"].append(cb)
#     for date in data["Document Date"]:
#         result_dict["Document Date"].append(date)
#     for hotel_name in data["HA_HOTELNAME"]:
#         result_dict["HA_HOTELNAME"].append(hotel_name)
#     for display_locale in data["HR_DISPLAYLOCALE"]:
#         result_dict["HR_DISPLAYLOCALE"].append(display_locale)
#     for tspid in data["HR_TSPID"]:
#         result_dict["HR_TSPID"].append(tspid)
#     for title in data["REVIEW_TITLE"]:
#         result_dict["REVIEW_TITLE"].append(title)
#     for sent in data["Sentence"]:
#         result_dict["Sentence"].append(sent)
#     for verbatim_type in data["VerbatimType"]:
#         result_dict["VerbatimType"].append(verbatim_type)
#     for verbatim in data["Verbatim"]:
#         result_dict["Verbatim"].append(verbatim)
#
# # Create a dataframe from the final dictionary and create CSV
# df = pd.DataFrame(result_dict)
# df.to_csv("test_compressed.csv")

#TODO 1. Format the data during the process

formatted_dict = {
    "Review ID": [],
    "Review Submission Date Time": [],
    "Account ID": [],
    "Validated Listing ID": []
}

# get the files
path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))

# For each file, extract all information from row 14 onwards
for f in csv_files:
    new_item = pd.read_csv(f, skiprows=13)
    data = pd.DataFrame(new_item)
    # Push each column to relevant list in dictionary
    for natural in data.NaturalId:
        formatted_dict["Review ID"].append(natural)
    #TODO 2. Format the date
    for date in data["Document Date"]:
        # Extract date element from the string
        date_str = re.search(r"\d{2}/\d{2}/\d{4}", date)
        res = datetime.strptime(date_str.group(), "%d/%m/%Y").date()
        x = (f"{res.strftime('%x')}T01:00:00.000GMT")
        formatted_dict["Review Submission Date Time"].append(x)
    for adm in data.ADM_EXPEDIAHOTELID:
        formatted_dict["Account ID"].append(adm)
        formatted_dict["Validated Listing ID"].append(adm)

mf = pd.DataFrame(formatted_dict)
mf.to_csv("compressed_test.csv")