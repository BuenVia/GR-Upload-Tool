import requests, os
from tkinter import messagebox
from tkinter import *
from format_csv import FormatCsv
from dotenv import load_dotenv, dotenv_values

# Env Varaiables
load_dotenv()
config = dotenv_values(".env")

# URL for API 
ENDPOINT = "http://localhost:9000/api"

# Reference to API keys - not necessary for demo version
header = { "Authorization": f"Bearer {config['API_KEY_ENV']}" }

# Class that calls reviews via API call and then calls the full verbatim for each review before putting it in to a list. The list is then passed to the FormatCsv class.
class ReviewFinder:
    
    def __init__(self):
        self.data_list = []
        self.review_list = []
        self.total = 0
        self.processed = 0
        self.scroll_id = ""
    
    # API call to get reviews
    def call_sentences(self, model, start_date, end_date, info_label):
        self.parameters = {
            "models": model,
            "created_since": start_date,
            "created_before": end_date,
            "leaf_only": "true",
            "attributes": "all",
            "scroll_id": self.scroll_id
        }
        
        if model == "H&S VRBO Model - REF" or model == "Health and Safety - Ref":
            self.response = requests.get(url=ENDPOINT, headers=header, params=self.parameters)
        self.data = self.response.json()
        self.total = self.data["total_count"]
        self.handler(self.data, model, start_date, end_date, info_label)
    
    # If call_sentences returns more than 1000 per page, add restuls to data_list list and paginate  
    def handler(self, ret_data, model, start_date, end_date, info_label):
        for sentence in ret_data["sentences"]:
            self.data_list.append(sentence)
        # if ret_data["page_size"] == 1000:
        #     self.scroll_id = ret_data["scroll_id"]
        #     self.call_sentences(model, start_date, end_date, info_label)
        # else:
        self.format_review(self.data_list, model, info_label, start_date)
        
    # Display process data on the GUI        
    def show_message(self, info_label, msg, clr):
        info_label.config(text=msg, bg=clr)

    # Show the number completed in the terminal
    def show_processed(self):
        self.processed += 1
        print(f"Completed: {self.processed} of {self.total}")
        return f"Completed: {self.processed} of {self.total}"


    # Format the data
    def format_review(self, data_list, model, info_label, start_date):
        self.show_message(info_label, f"Running...\nTotal Results: {self.total}\nOnce processing has finished, the file directory will open automatically", "yellow")
        runProcess = messagebox.askyesno(title="Begin Format", message=f"Total Reviews for {model}: {self.total}\n\nTotal processing time will be around {self.total} seconds.\n\nDo you wish to begin?.")
        if runProcess:
            # for sentence in data_list[:10]: #Limited to 10 results - to be kept for testing
            for sentence in data_list:
                new_sentence = sentence["attributes"]
                new_sentence["topic"] = sentence["classifications"][model][0]
                # if "natural_id" in new_sentence:
                #     new_sentence['verbatim'] = self.call_verbatim(new_sentence["natural_id"])                
                # else:
                #     new_sentence["verbatim"] = ""
                self.show_processed()
                self.review_list.append(new_sentence)
            FormatCsv(self.review_list, model, start_date)
            self.show_message(info_label, f"Completed. Total: {self.total}", "green")
            # Set the __init__ variables back to default setting
            self.review_list = []
            self.total = 0
            self.processed = 0
            self.show_files()
        else:
            self.review_list = []
            self.total = 0
            self.processed = 0
            self.show_message(info_label, "", "white")
            return

    # Sorts the full verbatim
    # def sort_verbatim(self, sentence):
    #     return sentence["sentence_start_pos"]
    
    # API call to get all text for a specific review
    # def call_verbatim(self, review_id):
    #     self.verbatim_parameters = {
    #         "query": f"natural_id:{review_id}",
    #         "fields": "all"
    #     }
    #     self.verbatim_response = requests.get(url=ENDPOINT, headers=header, params=self.verbatim_parameters)
    #     self.verbatim_data = self.verbatim_response.json()['sentences']
    #     self.verbatim_data.sort(key=self.sort_verbatim)

    #     full_verbatim = [sentence['sentence'] for sentence in self.verbatim_data]
    #     return " ".join(full_verbatim)

    # Once both the review_finder and format_csv stages have completed, the directory folder opens
    def show_files(self):
        path = "./uploads/"
        path = os.path.realpath(path)
        os.startfile(path)