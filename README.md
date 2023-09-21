# GR-Upload-Tool

An app built in Python that makes and API call to Qualtrics' XMD, a text analytics too, and receives back data in JSON form. The data is then manipulated and returned from the app in .csv format which is mapped to SalesForce requirements for Dataloader.

## Contents
- [Design](#design)
- [Install]{#install}
- [Use](#use)

## Design
The design concept of the app and it's codebase is broken down in to 3 areas:
1. GUI
2. API Call
3. Data format

The user will open the app and be presented with the GUI where they can select the dates they wish to export for and the model they wish to export from. 
An API call is then made to Qualtrics XMD and the relevant data is return in JSON format.
The data is then passed to a function which manipulates it in to the neccessary format for entry in SalesForce and returns the data in .csv form using Pandas.

## Install
	| Package | Command | 
    | ----------- | ----------- |
    | Pandas | pip install pandas |
    | Tkinter | pip install tk |    
    | Tkcalendar | pip install tkcalendar |    
    | Requests | pip install requests |    
    | Dotenv | pip install python-dotenv |    


## Use
This is a demo version of the app and is not connected to Qualtrics XMD. A fully deployed version is available. Please contact me for further information.
Run by exucting `python main.py` in the terminal