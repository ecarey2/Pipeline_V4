import openpyxl
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import glob
import os
import re
import csv


'''Module info: This module is for gathering user input for Pipeline script. Will prompt the user for a series of inputs to set up file paths
and load in appropriate csv files'''

def conversion_rate():
    ''' gets user input for phone or behavior camera used ot set conversion framerate used in subsequent calculations'''
    user_input = input("Please enter behavior imaging framerate to use: ")
    print("\nYou entered: ", user_input)
    conversion = float(user_input)

    return conversion

def imaging_rate():
    ''' gets user input for imaging framerate used in subsequent calculations'''
    user_input2 = input("Please enter imaging framerate to use: ")
    print("\nYou entered: ", user_input2)
    conversion2 = float(user_input2)

    return conversion2


def select_excel_file():
    '''select_excel_file function: This function gets user input for the file path 
    and name of behavior sheet to load in for further calculations and analysis
    Note: place excel sheet in same folder as python pipeline file
    '''

    # Create the main application window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt the user to select an Excel file
    file_path = filedialog.askopenfilename(
        title="Select an Excel file",
        filetypes=(("Excel files", "*.xlsx *.xls"), ("All files", "*.*"))
    )
    
    if file_path:
        print("Selected file:", file_path)
        return file_path
    else:
        print("No file selected.")
        return None
    


def select_sheets():
    '''getting user input for what animal sheet to analyze from behavior excel sheet'''

    sheet = input('\nEnter Excel sheet name to analyze, be sure spelling is correct. For example TGP#1_day5: ')

    return sheet



def data_input():
    ''' have user input if they want to filter df/f plots based on different ethogram scoring from behavior sheet'''

    user_input2 = input('\nIf you want to analyze withdrawal score, input that number (0-15) or N: ')
    withdrawal_s = user_input2
    user_input3 = input('\nIf you want to analyze stimulus score, input that number (0-4) or N: ')
    stim_s = user_input3
    user_input4 = input('\nDo you want to look at other ethograms Y or N? ')
    ethogram = user_input4


    return withdrawal_s, stim_s, ethogram


def get_specific_folders(base_path):
    '''have user input what trials to plot for df/f traces, make sure folders set up like "data1, data2 ...., data28
        as subfolders in same directory as the python script in folder named 'traces'
        - get user input for number of trials this will be the number of data1....data[i] folders in the directory
        - so if you have 28 subfolders put 28'''
    
    user_input = input(
        "\nEnter specific data folder numbers to analyze (e.g., 3, 5, 6 or 3-6): "
    )
    try:
        folder_indices = set()  # Use a set to avoid duplicates

        # Split the input by commas and process each part
        for part in user_input.split(","):
            part = part.strip()
            if "-" in part:  # If the part is a range
                start, end = map(int, part.split("-"))
                folder_indices.update(range(start, end + 1))  # Add the range of values
            else:  # Otherwise, it's a single value
                folder_indices.add(int(part))

        # Generate folder paths based on parsed indices
        selected_folders = [
            os.path.join(base_path, f"data{num}") for num in sorted(folder_indices)
        ]

        # Check if all selected folders exist
        missing_folders = [folder for folder in selected_folders if not os.path.exists(folder)]
        if missing_folders:
            print(f"The following folders do not exist: {missing_folders}")
            return []

        return selected_folders

    except ValueError:
        print("Invalid input. Please enter comma-separated numbers or ranges (e.g., 3, 5, 6 or 3-6).")
        return []
    

def injected_analysis_input():
    '''This function will take in user input to see if they are inputting uninjected vs injected dataset to set up downstream analysis'''
    user_input_injected = input('\nAre you analyzing injected or uninjected data? (Enter i for injected or u for uninjected): ')
    data_type = user_input_injected

    return data_type


def area_mat():
    '''This function will have user indicate path for .mat mask file containing region1 and region2 
    information for future area normalization calculations'''
      # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open folder selection dialog
    folder_selected = filedialog.askdirectory(title="Select Folder Containing .mat Files")

    if not folder_selected:
        print("No folder selected.")
        return []

    # Search for .mat files
    mat_files = glob.glob(os.path.join(folder_selected, "*.mat"))

    print(f"Found {len(mat_files)} .mat file(s) in: {folder_selected}")
    return mat_files


