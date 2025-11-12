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

#Nov 11 2025 the timing 40FPS work on inputting as user defined




def delay(onset_dict, d, data_key, conversion2):
    '''Calculates delay of event, using 40 FPS as conversion to seconds since that
    is what was used in AQuA2 for temporal timing'''
    # Get the onset time from the dictionary

    onset_time = onset_dict.get(data_key)
    
    if onset_time is None:
        # If no onset time is found for this data key, return None for all delays
        return [None] * len(d.columns)

    # Assuming the starting frames are in the first row of the DataFrame `d`
    starting_frames = pd.to_numeric(d.loc['Starting Frame'].values, errors='coerce')
    
    # Calculate delay by subtracting the starting frame from the onset time
    delays = []
    for start_frame in starting_frames:
        if pd.notna(start_frame):
            event_time = start_frame/conversion2 # used to be start_frame/40
            delay = event_time - onset_time  # Convert frame number to time in seconds
            if delay >= -2 and  delay <=3: #only look at the events correlated to the stimulus up to 4 seconds after stimulus
                delays.append(delay)
            else:
                #delays.append(-1)
                delays.append(None)
        else:
            delays.append(None)  # Handle missing start frame
    
    return delays



def l_analysis(df):
    '''Function that does analysis for delay left side events
    Takes in data frame and returns event, max df/f of event, duration of that event, area of event
    '''
    #df = df.set_index('Channel')
    event = df.loc['Index']
    max = df.loc['Curve - Max Dff']
    duration = df.loc[r'Curve - Duration 10% to 10% based on averge dF/F']
    area = df.loc['Ratio']
    delay = df.loc['delay']
    #print(event, max)
    return (event, max, duration, area, delay)




def process_data(conversion2,d,area1, area2, file, added, list, onset_dict, region, total_count_l_var, stim_count_l_var, 
                 percent_count_l_var, total_count_r_var, stim_count_r_var, percent_count_r_var, percent_response, total_count_l_var_area, total_count_r_var_area, left_list, right_list, events_passed_threshold_left, events_passed_threshold_r):

    """
    Processes a list of files, filtering based on 'Basic - Area', computing delay, 
    and updating relevant count variables.

    Args:
        d = dataframe = dataframe of events for given dataset
        file = csv read in
        added = boolean flag to avoid double counting
        list: List of data keys to match in file names.
        onset_dict (dict): Dictionary containing onset times.
        region (str): Region identifier ('region_1' or 'region_2').
        total_count_var (int): tracking total events before stim window filtering and area filtering.
        stim_count_var (int): tracking total events responding to stim after stim window filtering.
        percent_count_var (int): Tracks percentage count.
        percent_response (dict): Dictionary tracking responses to stim.
    """
    dataset_counted = False
    for j in list:
        if j in file and not added:
            data_key = j
            #print(data_key)
            #adding delay column
            if 'Basic - Area' in d.index:
                if region == 'region_1':
                    total_count_l_var += len(d.columns)
                    # Compute ratio for area normalization

                    d.loc['Ratio'] = (d.loc['Basic - Area'] / area1)*100
                    # Drop columns where the area ratio is less than 30%
                    d= d.drop(columns = d.columns[d.loc['Ratio'] < 25])
                    #d= d.drop(columns = d.columns[d.loc['Basic - Area'] < 250000])
                    total_count_l_var_area += len(d.columns)
                    if total_count_l_var_area == 0: #skip if total dataframe columns is zero after filtering area
                        continue
               
                    calculated_delays = delay(onset_dict, d, data_key, conversion2)
                #   print(calculated_delays)
                    if not d.empty and not d.columns.empty:
                        d.loc['delay'] = calculated_delays
                        d = d.dropna(axis = 1, subset = ['delay'])
                        stim_count_l_var += len(d.columns)
                        #(stim_count_l_var)
                        #if stim_count_l_var > 0 and not dataset_counted:
                        if len(d.columns)>0 and not dataset_counted:
                            percent_count_l_var += 1
                            percent_response[data_key] = 1
                            dataset_counted = True
                            #print(f" Added {data_key} to percent_count_l_var. New count: {percent_count_l_var}")
                            events_passed_threshold_left[data_key] = d.loc['Index']
                        left_list.append(d)
                    #print(d)
                else:
                    total_count_r_var += len(d.columns)
                    d.loc['Ratio'] = (d.loc['Basic - Area']/area2)*100
                    d = d.drop(columns = d.columns[d.loc['Ratio']< 25])
                    #d = d.drop(columns = d.columns[d.loc['Basic - Area'] < 250000])
                    total_count_r_var_area += len(d.columns)
                    if total_count_r_var_area == 0:
                        continue

                    calculated_delays = delay(onset_dict, d, data_key, conversion2)
                    if not d.empty and not d.columns.empty:
                        d.loc['delay'] = calculated_delays
                        d = d.dropna(axis =1, subset = ['delay'])
                        stim_count_r_var += len(d.columns)
                        print(data_key, len(d.columns))
                        #print(stim_count_l_var)
                        if len(d.columns) >0 and not dataset_counted:
                            percent_count_r_var += 1
                            percent_response[data_key] = 1
                            #print(f"Added {data_key} to percent_count_r_var. New count: {percent_count_r_var}")
                            dataset_counted = True
                            events_passed_threshold_r[data_key] = d.loc['Index']
                        right_list.append(d)
            added = True
            break
            

    return (d, total_count_l_var, stim_count_l_var, percent_count_l_var, total_count_r_var, stim_count_r_var, percent_count_r_var, percent_response, total_count_l_var_area, total_count_r_var_area, left_list, right_list, events_passed_threshold_left, events_passed_threshold_r)