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

#importing custom modules
import uiModule
import ethoModule
import left_rightModule
import PlottingModule
import Area_converter

#getting user input to set up file paths/load in behavior excel sheet
conversion = uiModule.conversion_rate() # behavior fr
conversion2 = uiModule.imaging_rate() # imaging fr
file_path = uiModule.select_excel_file()

if file_path:
    # Read the selected Excel file into a pandas DataFrame
    xls = pd.ExcelFile(file_path)
    print("Dataframe loaded successfully.")
    
else:
    print("No Excel file to load.")


sheet1 = uiModule.select_sheets()

#separate animal excel sheet into dataframe for analysis
df1 = pd.read_excel(xls, sheet1)
#renaming the first row in each sheet as the column names
df1.columns = df1.iloc[0]
df1 = df1[1:]

print(df1.head(2))

#Filter for ethograms
withdrawal_score, stim_score, etho = uiModule.data_input() #11-11-25 make sure this filtering is happening

#user input to see what type of data analyzing
#i is injected u is uninjected
dataset = uiModule.injected_analysis_input() 

#if data set is u then analyzing uninjected dataset, else either D110A or iBARK
if dataset == 'u':
    #constants for comparison with left and right analysis later
    ipsilateral_uninjected = 'region_1'
    contralateral_uninjected = 'region_2'
else:
    ipsilateral_injected= 'region_1'
    ipsilateral_uninjected = 'region_2'
    contralateral_injected = 'region_3'
    contralateral_uninjected = 'region_4'

#getting area of regions for later calculations
mat_data = uiModule.area_mat()
num, area1 = Area_converter.compute_area_from_mat_region1(mat_data,1.62)
num2, area2 = Area_converter.compute_area_from_mat_region2(mat_data,1.62)
if dataset != 'u':
    num3, area3 = Area_converter.compute_area_from_mat_region3(mat_data, 1.62)
    num4, area4 = Area_converter.compute_area_from_mat_region4(mat_data, 1.62)
    

# Base path to your data folders ** TODO update this for your directory **
# if don't want to do need a dummy folder in place
base_path = '/Users/erincarey/Documents/bphon/MK_invivo/Regions/traces'


# Get specific df/f trace folders from the user
folders = uiModule.get_specific_folders(base_path)
#print(folders)

#Filtering scored ethograms
ethogram_list = df1.columns.tolist()
count = ethoModule.count_partial_eth(ethogram_list, 'Ethogram')



# list to filter based on what foot is stimulated
left_foot = []
right_foot = []

for folder in folders:
    left, right = ethoModule.excel_loop_dff(folder, withdrawal_score, df1, stim_score, etho, conversion,conversion2, count)
    if left != '':
        left_foot.append(left)
    else:
        right_foot.append(right)


#########################################
#LEFT V RIGHT analysis from AQuA2 output#
#########################################

# **** user defined input here *****
#directory = '/Users/erincarey/Documents/bphon/daniela_pphipe_test/2025_new_chronic/Regions_real'
directory = '/Users/erincarey/Documents/bphon/3. Uninjured GGC Data_11_7_2025/GGC#1_day0/out'


csvs = glob.glob(os.path.join(directory, '*.xlsx'))

# Extract stimulus columns based on the understanding that 'B','8', '11', '5' are different stimuli and what foot stimulated
data_B_left_leg = df1[(df1['Stimulus'] == 'B') & (df1['Leg'] == 'L')]['Data'].tolist()
data_B_right_leg = df1[(df1['Stimulus'] == 'B') & (df1['Leg'] == 'R')]['Data'].tolist()
data_vf8_left_leg = df1[(df1['Stimulus'] == 8) & (df1['Leg'] == 'L')]['Data'].tolist()
data_vf8_right_leg = df1[(df1['Stimulus'] == 8) & (df1['Leg'] == 'R')]['Data'].tolist()
#data_vf11_left_leg = df1[(df1['Stimulus'] == 11) & (df1['Leg'] == 'L')]['Data'].tolist()
#data_vf11_right_leg = df1[(df1['Stimulus'] == 11) & (df1['Leg'] == 'R')]['Data'].tolist()
data_vf11_left_leg = df1[(df1['Stimulus'] == 'TP') & (df1['Leg'] == 'L')]['Data'].tolist()
data_vf11_right_leg = df1[(df1['Stimulus'] == 'TP') & (df1['Leg'] == 'R')]['Data'].tolist()
data_vf5_left_leg =  df1[(df1['Stimulus'] == 5) & (df1['Leg'] == 'L')]['Data'].tolist()
data_vf5_right_leg = df1[(df1['Stimulus'] == 5) & (df1['Leg'] == 'R')]['Data'].tolist()


# Convert the lists of numbers to strings formatted as 'dataXX' for later comparison with AQuA2 outputs
data_B_str_l = [f'data{str(num).zfill(2)}' for num in data_B_left_leg]
data_B_str_r = [f'data{str(num).zfill(2)}' for num in data_B_right_leg]
data_vf5_str_l = [f'data{str(num).zfill(2)}' for num in data_vf5_left_leg]
data_vf5_str_r = [f'data{str(num).zfill(2)}' for num in data_vf5_right_leg]
data_vf8_str_l = [f'data{str(num).zfill(2)}' for num in data_vf8_left_leg]
data_vf8_str_r = [f'data{str(num).zfill(2)}' for num in data_vf8_right_leg]
data_vf11_str_l = [f'data{str(num).zfill(2)}' for num in data_vf11_left_leg]
data_vf11_str_r = [f'data{str(num).zfill(2)}' for num in data_vf11_right_leg]
#data_vf11_str_l = [f'data{str(num).zfill(2)}' for num in data_vf11_left_leg]
#data_vf11_str_r = [f'data{str(num).zfill(2)}' for num in data_vf11_right_leg]

# print(data_B_str_l)
# print(data_B_str_r)
# print(data_vf5_str_l)
# print(data_vf5_str_r)
# print(data_vf8_str_l)
# print(data_vf8_str_r)
# print(data_vf11_str_l)
# print(data_vf11_str_r)

# Now, proceed to create the dictionary to store onset time
# Define the stimuli categories and corresponding data lists
stimuli = {
    'B': 'B',
    'vf8': 8,
    #'vf11': 11,
    'Tail Pinch': 'T',
    'vf5': 5
}

stimuli_data = {key: [f'data{str(num).zfill(2)}' for num in df1[df1['Stimulus'] == val]['Data']] for key, val in stimuli.items()}

# Create an empty dictionary to store the result
onset_dict = {}

# Loop over each stimulus and add entries to the dictionary
for label, stimulus in stimuli.items():
    data_list = df1[df1['Stimulus'] == stimulus]['Data'].tolist()
    for num in data_list:
        key = f'data{str(num).zfill(2)}'
        #convert to seconds
        value = df1[df1['Data'] == num]['Onset'].values[0]/conversion
        onset_dict[key] = value
        #print(value)

#delete this later only for debugging
print(onset_dict)


#counters to determine % events responding to stimulus

#brush left foot
total_brush_left_l_count = 0
stim_brush_left_l_count = 0
percent_brush_left_l_count = 0
total_count_l_b_area = 0
total_brush_left_r_count = 0
stim_brush_left_r_count = 0
percent_brush_left_r_count = 0
total_count_r_b_area = 0

#brush right foot
total_brush_right_l_count = 0
stim_brush_right_l_count = 0
percent_brush_right_l_count = 0
total_count_rl_b_area = 0
total_brush_right_r_count = 0
stim_brush_right_r_count = 0
percent_brush_right_r_count = 0
total_count_rr_b_area = 0

#vf5 left foot
total_vf5_left_l_count = 0
stim_vf5_left_l_count = 0
percent_vf5_left_l_count = 0
total_vf5_l_b_area = 0
total_vf5_left_r_count = 0
stim_vf5_left_r_count = 0
percent_vf5_left_r_count = 0
total_vf5_r_b_area = 0

#vf5 right foot
total_vf5_right_l_count = 0
stim_vf5_right_l_count = 0
percent_vf5_right_l_count = 0
total_vf5_rl_b_area = 0
total_vf5_right_r_count = 0
stim_vf5_right_r_count = 0
percent_vf5_right_r_count = 0
total_vf5_rr_b_area = 0

#vf8 left foot
total_vf8_left_l_count = 0
stim_vf8_left_l_count = 0
percent_vf8_left_l_count = 0
total_vf8_l_b_area = 0
total_vf8_left_r_count = 0
stim_vf8_left_r_count = 0
percent_vf8_left_r_count = 0
total_vf8_r_b_area = 0

#vf8 right foot
total_vf8_right_l_count = 0
stim_vf8_right_l_count = 0
percent_vf8_right_l_count = 0
total_vf8_rl_b_area = 0
total_vf8_right_r_count = 0
stim_vf8_right_r_count = 0
percent_vf8_right_r_count = 0
total_vf8_rr_b_area = 0

#vf11 left foot for MKs is Pin Prick
total_vf11_left_l_count = 0
stim_vf11_left_l_count = 0
percent_vf11_left_l_count = 0
total_vf11_l_b_area = 0
total_vf11_left_r_count = 0
stim_vf11_left_r_count = 0
percent_vf11_left_r_count = 0
total_vf11_r_b_area = 0

#vf11 right foot for MKs is Pin Prick
total_vf11_right_l_count = 0
stim_vf11_right_l_count = 0
percent_vf11_right_l_count = 0
total_vf11_rl_b_area = 0
total_vf11_right_r_count = 0
stim_vf11_right_r_count = 0
percent_vf11_right_r_count = 0
total_vf11_rr_b_area = 0


percent_response = {}
events_passed_threshold_left = {}
events_passed_threshold_r = {}

#store filtered datasets for plotting
left_brush_l_side = []
right_brush_l_side = []
right_brush_r_side = []
left_brush_r_side = []
left_11_l_side = []
right_11_l_side = []
left_11_r_side = []
right_11_r_side = []
left_5_l_side = []
right_5_l_side = []
left_5_r_side = []
right_5_r_side = []
left_8_l_side = []
right_8_l_side = []
left_8_r_side = []
right_8_r_side = []

# Loop over each stimulus and add entries to the percet_response dictionary
for label, stimulus in stimuli.items():
    data_list = df1[df1['Stimulus'] == stimulus]['Data'].tolist()
    for num in data_list:
        key = f'data{str(num).zfill(2)}'
        #set all counts for percent response to 0
        value = 0
        percent_response[key] = value
        events_passed_threshold_left[key] = []
        events_passed_threshold_r[key] = []

# Function to categorize data
for file in csvs:
    d = pd.read_excel(file)
    d = d.set_index('Channel')

     # Check if the file belongs to region1 or region2
    if 'region_1' in file:
         region = 'region_1'
    else:
        region = 'region_2'

    added = False # flag to avoid double counting

    #filtering events for area and time window
    d, total_brush_left_l_count, stim_brush_left_l_count, percent_brush_left_l_count, total_brush_left_r_count, stim_brush_left_r_count, percent_brush_left_r_count, percent_response, total_count_l_b_area, total_count_r_b_area, left_brush_l_side, left_brush_r_side, events_passed_threshold_left, events_passed_threshold_r= left_rightModule.process_data(conversion2, d, area1, area2, file, added, data_B_str_l, onset_dict, region, total_brush_left_l_count, stim_brush_left_l_count,
                                  percent_brush_left_l_count, total_brush_left_r_count, stim_brush_left_r_count, percent_brush_left_r_count, percent_response, total_count_l_b_area, total_count_r_b_area, left_brush_l_side, left_brush_r_side, events_passed_threshold_left, events_passed_threshold_r)
    
    d, total_brush_right_l_count, stim_brush_right_l_count, percent_brush_right_l_count, total_brush_right_r_count, stim_brush_right_r_count, percent_brush_right_r_count, percent_response, total_count_rl_b_area, total_count_rr_b_area, right_brush_l_side, right_brush_r_side, events_passed_threshold_left, events_passed_threshold_r = left_rightModule.process_data(conversion2, d, area1, area2, file, added, data_B_str_r, onset_dict, region, total_brush_right_l_count, stim_brush_right_l_count, 
                                 percent_brush_right_l_count, total_brush_right_r_count, stim_brush_right_r_count, percent_brush_right_r_count, percent_response, total_count_rl_b_area, total_count_rr_b_area, right_brush_l_side, right_brush_r_side, events_passed_threshold_left, events_passed_threshold_r)
    
    d, total_vf5_left_l_count, stim_vf5_left_l_count, percent_vf5_left_l_count, total_vf5_left_r_count, stim_vf5_left_r_count, percent_vf5_left_r_count, percent_response, total_vf5_l_b_area, total_vf5_r_b_area, left_5_l_side, left_5_r_side, events_passed_threshold_left, events_passed_threshold_r = left_rightModule.process_data(conversion2, d, area1, area2, file, added, data_vf5_str_l, onset_dict, region, total_vf5_left_l_count, stim_vf5_left_l_count,
                                   percent_vf5_left_l_count, total_vf5_left_r_count, stim_vf5_left_r_count, percent_vf5_left_r_count, percent_response, total_vf5_l_b_area, total_vf5_r_b_area, left_5_l_side, left_5_r_side, events_passed_threshold_left, events_passed_threshold_r)
    
    d, total_vf5_right_l_count, stim_vf5_right_l_count, percent_vf5_right_l_count, total_vf5_right_r_count, stim_vf5_right_r_count, percent_vf5_right_r_count, percent_response, total_vf5_rl_b_area, total_vf5_rr_b_area, right_5_l_side, right_5_r_side, events_passed_threshold_left, events_passed_threshold_r = left_rightModule.process_data(conversion2, d, area1, area2, file, added, data_vf5_str_r, onset_dict, region, total_vf5_right_l_count, stim_vf5_right_l_count, 
                                percent_vf5_right_l_count, total_vf5_right_r_count, stim_vf5_right_r_count, percent_vf5_right_r_count, percent_response, total_vf5_rl_b_area, total_vf5_rr_b_area, right_5_l_side, right_5_r_side, events_passed_threshold_left, events_passed_threshold_r)

    d, total_vf8_left_l_count, stim_vf8_left_l_count, percent_vf8_left_l_count, total_vf8_left_r_count, stim_vf8_left_r_count, percent_vf8_left_r_count, percent_response, total_vf8_l_b_area, total_vf8_r_b_area, left_8_l_side, left_8_r_side, events_passed_threshold_left, events_passed_threshold_r = left_rightModule.process_data(conversion2, d, area1, area2, file, added, data_vf8_str_l, onset_dict, region, total_vf8_left_l_count, stim_vf8_left_l_count,
                                  percent_vf8_left_l_count, total_vf8_left_r_count, stim_vf8_left_r_count, percent_vf8_left_r_count, percent_response, total_vf8_l_b_area, total_vf8_r_b_area, left_8_l_side, left_8_r_side, events_passed_threshold_left, events_passed_threshold_r)
    
    d, total_vf8_right_l_count, stim_vf8_right_l_count, percent_vf8_right_l_count, total_vf8_right_r_count, stim_vf8_right_r_count, percent_vf8_right_r_count, percent_response, total_vf8_rl_b_area, total_vf8_rr_b_area, right_8_l_side, right_8_r_side, events_passed_threshold_left, events_passed_threshold_r = left_rightModule.process_data(conversion2, d, area1, area2, file, added, data_vf8_str_r, onset_dict, region, total_vf8_right_l_count, stim_vf8_right_l_count, 
                                 percent_vf8_right_l_count, total_vf8_right_r_count, stim_vf8_right_r_count, percent_vf8_right_r_count, percent_response, total_vf8_rl_b_area, total_vf8_rr_b_area, right_8_l_side, right_8_r_side, events_passed_threshold_left, events_passed_threshold_r)
    
    d, total_vf11_left_l_count, stim_vf11_left_l_count, percent_vf11_left_l_count, total_vf11_left_r_count, stim_vf11_left_r_count, percent_vf11_left_r_count, percent_response, total_vf11_l_b_area, total_vf11_r_b_area, left_11_l_side, left_11_r_side, events_passed_threshold_left, events_passed_threshold_r= left_rightModule.process_data(conversion2, d, area1, area2, file, added, data_vf11_str_l, onset_dict, region, total_vf11_left_l_count, stim_vf11_left_l_count,
                                  percent_vf11_left_l_count, total_vf11_left_r_count, stim_vf11_left_r_count, percent_vf11_left_r_count, percent_response, total_vf11_l_b_area, total_vf11_r_b_area, left_11_l_side, left_11_r_side, events_passed_threshold_left, events_passed_threshold_r)
    
    d, total_vf11_right_l_count, stim_vf11_right_l_count, percent_vf11_right_l_count, total_vf11_right_r_count, stim_vf11_right_r_count, percent_vf11_right_r_count, percent_response, total_vf11_rl_b_area, total_vf11_rr_b_area, right_11_l_side, right_11_r_side, events_passed_threshold_left, events_passed_threshold_r = left_rightModule.process_data(conversion2, d, area1, area2, file, added, data_vf11_str_r, onset_dict, region, total_vf11_right_l_count, stim_vf11_right_l_count, 
                                percent_vf11_right_l_count, total_vf11_right_r_count, stim_vf11_right_r_count, percent_vf11_right_r_count, percent_response, total_vf11_rl_b_area, total_vf11_rr_b_area, right_11_l_side, right_11_r_side, events_passed_threshold_left, events_passed_threshold_r)

#print statements delete later
print('Left list brush: ', data_B_str_l)
print('Right list brush: ',  data_B_str_r)
# print(total_brush_left_l_count, stim_brush_left_l_count)
# #print(f'percent responding: {percent_brush_left_l_count/len(data_B_str_l)}')
# print(total_brush_left_r_count, stim_brush_left_r_count)
# print(total_brush_right_l_count, stim_brush_right_l_count)
# print(total_brush_right_r_count, stim_brush_right_r_count)
print('percent right brush')
print(percent_brush_right_l_count, percent_brush_right_r_count)
print(stim_brush_right_l_count, stim_brush_right_r_count)  # correct for 
print('percent brush left')
print(percent_brush_left_l_count, percent_brush_left_r_count)
print(stim_brush_left_l_count, stim_brush_left_r_count)
print('Total Large Scale Events')
print(total_count_l_b_area)
print(stim_brush_left_l_count)
print(f'left brush ipsi: {total_count_l_b_area-stim_brush_left_l_count}')
print(f'left brush contra:{total_count_r_b_area-stim_brush_left_r_count}')
print(f'right brush ipsi: {total_count_rl_b_area-stim_brush_right_l_count}')
print(f'right brush contra: {total_count_rr_b_area-stim_brush_right_r_count}')



# print('vf5')
# print(total_vf5_l_b_area, total_vf5_r_b_area)
# print(stim_vf5_left_l_count, stim_vf5_left_r_count)
# print('vf11')
# print(total_vf11_l_b_area, total_vf11_r_b_area)
# print(stim_vf11_left_l_count, stim_vf11_left_r_count)

#save dictonary that has if each data has event in stim window 1 is yes 0 is no
percent_response = dict(sorted(percent_response.items()))
df_dict = pd.DataFrame.from_dict(percent_response, orient = 'index', columns = ['Series'])
path_dict = os.path.join(directory, 'percent_respond_per_trial.csv')
csv_path = df_dict.to_csv(path_dict, header = True)

#save dictionary of events per trial that pass filters
# Convert dictionary of Series into a structured DataFrame
df_events_sorted = dict(sorted(events_passed_threshold_left.items(), key=lambda x: str(x[0])))
df_events = pd.DataFrame({key: pd.Series(value) for key, value in df_events_sorted.items()})

# Transpose so that each row represents a data key with its values
df_events_vals = df_events.transpose()

# Save as CSV
path_dict1 = os.path.join(directory, 'events_respond_per_trial_region1_leftside.csv')
csv_path1 = df_events_vals.to_csv(path_dict1, header = True)
path_dict3 = os.path.join(directory, 'events_respond_per_trial_region1_leftside.txt')
csv_path3 = df_events_vals.to_csv(path_dict3,sep=' ', index = True, header = False)

#save right dictionary events
df_events2_sorted = dict(sorted(events_passed_threshold_r.items(), key=lambda x: str(x[0])))
#df_events2 = dict(sorted(events_passed_threshold_r.items()))
df_events2 = pd.DataFrame({key: pd.Series(value) for key, value in df_events2_sorted.items()})
#df_events2_values = df_events2.drop(columns = df_events2.columns[0], axis = 1)


# Transpose so that each row represents a data key with its values
df_events2_values = df_events2.transpose()



# Save as CSV
path_dict2 = os.path.join(directory, 'events_respond_per_trial_region2_rightside.txt')
csv_path2 = df_events2_values.to_csv(path_dict2,sep=' ', index = True, header = False)


#calling function for plotting and saving dataframes

delay_b_left_l, duration_b_left_l, area_b_left_l, dff_b_left_l = PlottingModule.left_right_list_sort(left_brush_l_side)
#print(delay_b_left_l)
dff_b_left_l = PlottingModule.flatten(dff_b_left_l)
duration_b_left_l = PlottingModule.flatten(duration_b_left_l)
delay_b_left_l = PlottingModule.flatten(delay_b_left_l)
area_b_left_l = PlottingModule.flatten(area_b_left_l)
if len(data_B_str_l) > 0:
    percent_respond_left_brush_l = (percent_brush_left_l_count / len(data_B_str_l)) * 100
else:
    percent_respond_left_brush_l = 0  # Or set to None if needed
#percent_respond_left_brush_l = (percent_brush_left_l_count/len(data_B_str_l)*100)


delay_b_left_r,duration_b_left_r, area_b_left_r, dff_b_left_r = PlottingModule.left_right_list_sort(left_brush_r_side)
dff_b_left_r = PlottingModule.flatten(dff_b_left_r)
duration_b_left_r = PlottingModule.flatten(duration_b_left_r)
delay_b_left_r = PlottingModule.flatten(delay_b_left_r)
area_b_left_r = PlottingModule.flatten(area_b_left_r)
#percent_respond_left_brush_r = (percent_brush_left_r_count/len(data_B_str_l)*100)
if len(data_B_str_l) > 0:
    percent_respond_left_brush_r = (percent_brush_left_r_count / len(data_B_str_l)) * 100
else:
    percent_respond_left_brush_r = 0  # Or set to None if needed

delay_b_right_l,duration_b_right_l, area_b_right_l, dff_b_right_l = PlottingModule.left_right_list_sort(right_brush_l_side)
dff_b_right_l = PlottingModule.flatten(dff_b_right_l)
duration_b_right_l = PlottingModule.flatten(duration_b_right_l)
delay_b_right_l = PlottingModule.flatten(delay_b_right_l)
area_b_right_l= PlottingModule.flatten(area_b_right_l)
#percent_respond_right_brush_l = (percent_brush_right_l_count/len(data_B_str_r)*100)
if len(data_B_str_r) > 0:
    percent_respond_right_brush_l = (percent_brush_right_l_count / len(data_B_str_r)) * 100
else:
    percent_respond_right_brush_l = 0  # Or set to None if needed


delay_b_right_r,duration_b_right_r, area_b_right_r, dff_b_right_r = PlottingModule.left_right_list_sort(right_brush_r_side)
dff_b_right_r = PlottingModule.flatten(dff_b_right_r)
duration_b_right_r = PlottingModule.flatten(duration_b_right_r)
delay_b_right_r = PlottingModule.flatten(delay_b_right_r)
area_b_right_r = PlottingModule.flatten(area_b_right_r)
#percent_respond_right_brush_r = (percent_brush_right_r_count/len(data_B_str_r)*100)
if len(data_B_str_r) > 0:
    percent_respond_right_brush_r = (percent_brush_right_r_count / len(data_B_str_r)) * 100
else:
    percent_respond_right_brush_r = 0 


# print(duration_b_left_l)
# print(duration_b_left_r)
# print(duration_b_right_l)
# print(duration_b_right_r)

#print(percent_respond_left_brush_l, percent_respond_left_brush_r, percent_respond_right_brush_l, percent_respond_right_brush_r)

all_dff_brush_values = np.concatenate([
    dff_b_left_l,
    dff_b_left_r, 
    dff_b_right_l, 
    dff_b_right_r
])

all_brush_dff_sides =  PlottingModule.plot_sides(dff_b_left_l, dff_b_left_r, dff_b_right_l, dff_b_right_r)

#plotting dff brush
data1 = {
    'value' : all_dff_brush_values,
    'Side of Spinal Cord': all_brush_dff_sides
}

PlottingModule.plot_dff_dataframe(data1, directory, 'Brush')

#plotting percent responding brush
brush_vars = [percent_respond_left_brush_l, percent_respond_left_brush_r, percent_respond_right_brush_l, percent_respond_right_brush_r]
print(brush_vars)
PlottingModule.plot_percent(brush_vars, directory, 'Brush')

#plotting duration brush
all_duration_brush_values = np.concatenate([
    duration_b_left_l, 
    duration_b_left_r, 
    duration_b_right_l, 
    duration_b_right_r
  
])

all_brush_duration_sides = PlottingModule.plot_sides(duration_b_left_l, duration_b_left_r, duration_b_right_l, duration_b_right_r)
data2 = {
    'value': all_duration_brush_values,
    'Side of Spinal Cord': all_brush_duration_sides
}

PlottingModule.plot_dur_dataframe(data2, directory, 'Brush')

#plotting area brush
all_area_brush_values = np.concatenate([
    area_b_left_l, 
    area_b_left_r, 
    area_b_right_l, 
    area_b_right_r
])

all_area_brush_sides = PlottingModule.plot_sides(area_b_left_l, area_b_left_r, area_b_right_l, area_b_right_r)
data3 = {
    'value': all_area_brush_values,
    'Side of Spinal Cord': all_area_brush_sides
}
PlottingModule.plot_area_dataframe(data3, directory, 'Brush')

#plotting delay brush
all_brush_delay_values = np.concatenate([
    delay_b_left_l, 
    delay_b_left_r, 
    delay_b_right_l, 
    delay_b_right_r
])

all_delay_brush_sides = PlottingModule.plot_sides(delay_b_left_l, delay_b_left_r, delay_b_right_l, delay_b_right_r)
data4 = {
    'value' : all_brush_delay_values, 
    'Side of Spinal Cord': all_delay_brush_sides
}
PlottingModule.plot_delay_dataframe(data4, directory, 'Brush')


##### Plotting VF 5 #############

delay_5_left_l, duration_5_left_l, area_5_left_l, dff_5_left_l = PlottingModule.left_right_list_sort(left_5_l_side)
#print(delay_b_left_l)
dff_5_left_l = PlottingModule.flatten(dff_5_left_l)
duration_5_left_l = PlottingModule.flatten(duration_5_left_l)
delay_5_left_l = PlottingModule.flatten(delay_5_left_l)
area_5_left_l = PlottingModule.flatten(area_5_left_l)
percent_respond_left_5_l = (percent_vf5_left_l_count / len(data_vf5_str_l) * 100) if len(data_vf5_str_l) else 0



delay_5_left_r,duration_5_left_r, area_5_left_r, dff_5_left_r = PlottingModule.left_right_list_sort(left_5_r_side)
dff_5_left_r = PlottingModule.flatten(dff_5_left_r)
duration_5_left_r = PlottingModule.flatten(duration_5_left_r)
delay_5_left_r = PlottingModule.flatten(delay_5_left_r)
area_5_left_r = PlottingModule.flatten(area_5_left_r)

percent_respond_left_5_r = (percent_vf5_left_r_count / len(data_vf5_str_l) * 100) if len(data_vf5_str_l) else 0


delay_5_right_l,duration_5_right_l, area_5_right_l, dff_5_right_l = PlottingModule.left_right_list_sort(right_5_l_side)
dff_5_right_l = PlottingModule.flatten(dff_5_right_l)
duration_5_right_l = PlottingModule.flatten(duration_5_right_l)
delay_5_right_l = PlottingModule.flatten(delay_5_right_l)
area_5_right_l= PlottingModule.flatten(area_5_right_l)
#percent_respond_right_5_l = (percent_vf5_right_l_count/len(data_vf5_str_r)*100)
percent_respond_right_5_l = (percent_vf5_right_l_count / len(data_vf5_str_r) * 100) if len(data_vf5_str_r) else 0



delay_5_right_r,duration_5_right_r, area_5_right_r, dff_5_right_r = PlottingModule.left_right_list_sort(right_5_r_side)
dff_5_right_r = PlottingModule.flatten(dff_5_right_r)
duration_5_right_r = PlottingModule.flatten(duration_5_right_r)
delay_5_right_r = PlottingModule.flatten(delay_5_right_r)
area_5_right_r = PlottingModule.flatten(area_5_right_r)
#percent_respond_right_5_r = (percent_vf5_right_r_count/len(data_vf5_str_r)*100)
percent_respond_right_5_r = (percent_vf5_right_r_count / len(data_vf5_str_r) * 100) if len(data_vf5_str_r) else 0



all_5_values = np.concatenate([
    dff_5_left_l,
    dff_5_left_r, 
    dff_5_right_l, 
    dff_5_right_r
])

all_5_dff_sides =  PlottingModule.plot_sides(dff_5_left_l, dff_5_left_r, dff_5_right_l, dff_5_right_r)

#plotting dff vf5
data5= {
    'value' : all_5_values,
    'Side of Spinal Cord': all_5_dff_sides
}

PlottingModule.plot_dff_dataframe(data5, directory, 'VF5')

#plotting percent responding vf5
vf5_vars = [percent_respond_left_5_l, percent_respond_left_5_r, percent_respond_right_5_l, percent_respond_right_5_r]
PlottingModule.plot_percent(vf5_vars, directory, 'VF5')

#plotting duration brush
all_duration_vf5_values = np.concatenate([
    duration_5_left_l, 
    duration_5_left_r, 
    duration_5_right_l, 
    duration_5_right_r
  
])

all_vf5_duration_sides = PlottingModule.plot_sides(duration_5_left_l, duration_5_left_r, duration_5_right_l, duration_5_right_r)
data6 = {
    'value': all_duration_vf5_values,
    'Side of Spinal Cord': all_vf5_duration_sides
}

PlottingModule.plot_dur_dataframe(data6, directory, 'VF5')

#plotting area brush
all_area_5_values = np.concatenate([
    area_5_left_l, 
    area_5_left_r, 
    area_5_right_l, 
    area_5_right_r
])

all_area_5_sides = PlottingModule.plot_sides(area_5_left_l, area_5_left_r, area_5_right_l, area_5_right_r)
data7 = {
    'value': all_area_5_values,
    'Side of Spinal Cord': all_area_5_sides
}
PlottingModule.plot_area_dataframe(data7, directory, 'VF5')

#plotting delay brush
all_5_delay_values = np.concatenate([
    delay_5_left_l, 
    delay_5_left_r, 
    delay_5_right_l, 
    delay_5_right_r
])

all_delay_5_sides = PlottingModule.plot_sides(delay_5_left_l, delay_5_left_r, delay_5_right_l, delay_5_right_r)
data8 = {
    'value' : all_5_delay_values, 
    'Side of Spinal Cord': all_delay_5_sides
}
PlottingModule.plot_delay_dataframe(data8, directory, 'VF5')

###### Plotting VF 8 ##########


delay_8_left_l, duration_8_left_l, area_8_left_l, dff_8_left_l = PlottingModule.left_right_list_sort(left_8_l_side)
#print(delay_b_left_l)
dff_8_left_l = PlottingModule.flatten(dff_8_left_l)
duration_8_left_l = PlottingModule.flatten(duration_8_left_l)
delay_8_left_l = PlottingModule.flatten(delay_8_left_l)
area_8_left_l = PlottingModule.flatten(area_8_left_l)
percent_respond_left_8_l = (percent_vf8_left_l_count/len(data_vf8_str_l)*100)


delay_8_left_r,duration_8_left_r, area_8_left_r, dff_8_left_r = PlottingModule.left_right_list_sort(left_8_r_side)
dff_8_left_r = PlottingModule.flatten(dff_8_left_r)
duration_8_left_r = PlottingModule.flatten(duration_8_left_r)
delay_8_left_r = PlottingModule.flatten(delay_8_left_r)
area_8_left_r = PlottingModule.flatten(area_8_left_r)
percent_respond_left_8_r = (percent_vf8_left_r_count/len(data_vf8_str_l)*100)

delay_8_right_l,duration_8_right_l, area_8_right_l, dff_8_right_l = PlottingModule.left_right_list_sort(right_8_l_side)
dff_8_right_l = PlottingModule.flatten(dff_8_right_l)
duration_8_right_l = PlottingModule.flatten(duration_8_right_l)
delay_8_right_l = PlottingModule.flatten(delay_8_right_l)
area_8_right_l= PlottingModule.flatten(area_8_right_l)
percent_respond_right_8_l = (percent_vf8_right_l_count/len(data_vf8_str_r)*100)


delay_8_right_r,duration_8_right_r, area_8_right_r, dff_8_right_r = PlottingModule.left_right_list_sort(right_8_r_side)
dff_8_right_r = PlottingModule.flatten(dff_8_right_r)
duration_8_right_r = PlottingModule.flatten(duration_8_right_r)
delay_8_right_r = PlottingModule.flatten(delay_8_right_r)
area_8_right_r = PlottingModule.flatten(area_8_right_r)
percent_respond_right_8_r = (percent_vf8_right_r_count/len(data_vf8_str_r)*100)


all_8_values = np.concatenate([
    dff_8_left_l,
    dff_8_left_r, 
    dff_8_right_l, 
    dff_8_right_r
])

all_8_dff_sides =  PlottingModule.plot_sides(dff_8_left_l, dff_8_left_r, dff_8_right_l, dff_8_right_r)

#plotting dff vf8
data9= {
    'value' : all_8_values,
    'Side of Spinal Cord': all_8_dff_sides
}

PlottingModule.plot_dff_dataframe(data9, directory, 'VF8')

#plotting percent responding vf8
vf8_vars = [percent_respond_left_8_l, percent_respond_left_8_r, percent_respond_right_8_l, percent_respond_right_8_r]
PlottingModule.plot_percent(vf8_vars, directory, 'VF8')

#plotting duration vf8
all_duration_vf8_values = np.concatenate([
    duration_8_left_l, 
    duration_8_left_r, 
    duration_8_right_l, 
    duration_8_right_r
  
])

all_vf8_duration_sides = PlottingModule.plot_sides(duration_8_left_l, duration_8_left_r, duration_8_right_l, duration_8_right_r)
data10 = {
    'value': all_duration_vf8_values,
    'Side of Spinal Cord': all_vf8_duration_sides
}

PlottingModule.plot_dur_dataframe(data10, directory, 'VF8')

#plotting area vf8
all_area_8_values = np.concatenate([
    area_8_left_l, 
    area_8_left_r, 
    area_8_right_l, 
    area_8_right_r
])

all_area_8_sides = PlottingModule.plot_sides(area_8_left_l, area_8_left_r, area_8_right_l, area_8_right_r)
data11 = {
    'value': all_area_8_values,
    'Side of Spinal Cord': all_area_8_sides
}
PlottingModule.plot_area_dataframe(data11, directory, 'VF8')

#plotting delay vf8
all_8_delay_values = np.concatenate([
    delay_8_left_l, 
    delay_8_left_r, 
    delay_8_right_l, 
    delay_8_right_r
])

all_delay_8_sides = PlottingModule.plot_sides(delay_8_left_l, delay_8_left_r, delay_8_right_l, delay_8_right_r)
data12 = {
    'value' : all_8_delay_values, 
    'Side of Spinal Cord': all_delay_8_sides
}
PlottingModule.plot_delay_dataframe(data12, directory, 'VF8')


#### Plotting VF11 ########
delay_11_left_l, duration_11_left_l, area_11_left_l, dff_11_left_l = PlottingModule.left_right_list_sort(left_11_l_side)
#print(delay_b_left_l)
dff_11_left_l = PlottingModule.flatten(dff_11_left_l)
duration_11_left_l = PlottingModule.flatten(duration_11_left_l)
delay_11_left_l = PlottingModule.flatten(delay_11_left_l)
area_11_left_l = PlottingModule.flatten(area_11_left_l)
#percent_respond_left_11_l = (percent_vf11_left_l_count/len(data_vf11_str_l)*100)
if len(data_vf11_str_l) > 0:
    percent_respond_left_11_l = (percent_vf11_left_l_count / len(data_vf11_str_l)) * 100
else:
    percent_respond_left_11_l = 0


delay_11_left_r,duration_11_left_r, area_11_left_r, dff_11_left_r = PlottingModule.left_right_list_sort(left_11_r_side)
dff_11_left_r = PlottingModule.flatten(dff_11_left_r)
duration_11_left_r = PlottingModule.flatten(duration_11_left_r)
delay_11_left_r = PlottingModule.flatten(delay_11_left_r)
area_11_left_r = PlottingModule.flatten(area_11_left_r)
#percent_respond_left_11_r = (percent_vf11_left_r_count/len(data_vf11_str_l)*100)
if len(data_vf11_str_l) > 0:
    percent_respond_left_11_r = (percent_vf11_left_r_count / len(data_vf11_str_l)) * 100
else:
    percent_respond_left_11_r = 0

delay_11_right_l,duration_11_right_l, area_11_right_l, dff_11_right_l = PlottingModule.left_right_list_sort(right_11_l_side)
dff_11_right_l = PlottingModule.flatten(dff_11_right_l)
duration_11_right_l = PlottingModule.flatten(duration_11_right_l)
delay_11_right_l = PlottingModule.flatten(delay_11_right_l)
area_11_right_l= PlottingModule.flatten(area_11_right_l)
#percent_respond_right_11_l = (percent_vf11_right_l_count/len(data_vf11_str_r)*100)
if len(data_vf11_str_r) > 0:
    percent_respond_right_11_l = (percent_vf11_right_l_count / len(data_vf11_str_r)) * 100
else:
    percent_respond_right_11_l = 0


delay_11_right_r,duration_11_right_r, area_11_right_r, dff_11_right_r = PlottingModule.left_right_list_sort(right_11_r_side)
dff_11_right_r = PlottingModule.flatten(dff_11_right_r)
duration_11_right_r = PlottingModule.flatten(duration_11_right_r)
delay_11_right_r = PlottingModule.flatten(delay_11_right_r)
area_11_right_r = PlottingModule.flatten(area_11_right_r)
#percent_respond_right_11_r = (percent_vf11_right_r_count/len(data_vf11_str_r)*100)
if len(data_vf11_str_r) > 0:
    percent_respond_right_11_r = (percent_vf11_right_r_count / len(data_vf11_str_r)) * 100
else:
    percent_respond_right_11_r = 0


all_11_values = np.concatenate([
    dff_11_left_l,
    dff_11_left_r, 
    dff_11_right_l, 
    dff_11_right_r
])

all_11_dff_sides =  PlottingModule.plot_sides(dff_11_left_l, dff_11_left_r, dff_11_right_l, dff_11_right_r)

#plotting dff vf11 or TP,  or pin prick for MK
data13= {
    'value' : all_11_values,
    'Side of Spinal Cord': all_11_dff_sides
}

PlottingModule.plot_dff_dataframe(data13, directory, 'Tail Pinch') #'VF11')

#plotting percent responding vf11
vf11_vars = [percent_respond_left_11_l, percent_respond_left_11_r, percent_respond_right_11_l, percent_respond_right_11_r]
PlottingModule.plot_percent(vf11_vars, directory, 'Tail Pinch')#'VF11')

#plotting duration vf11
all_duration_vf11_values = np.concatenate([
    duration_11_left_l, 
    duration_11_left_r, 
    duration_11_right_l, 
    duration_11_right_r
  
])

all_vf11_duration_sides = PlottingModule.plot_sides(duration_11_left_l, duration_11_left_r, duration_11_right_l, duration_11_right_r)
data14 = {
    'value': all_duration_vf11_values,
    'Side of Spinal Cord': all_vf11_duration_sides
}

PlottingModule.plot_dur_dataframe(data14, directory, 'Tail Pinch')#'VF11')

#plotting area vf11
all_area_11_values = np.concatenate([
    area_11_left_l, 
    area_11_left_r, 
    area_11_right_l, 
    area_11_right_r
])

all_area_11_sides = PlottingModule.plot_sides(area_11_left_l, area_11_left_r, area_11_right_l, area_11_right_r)
data15 = {
    'value': all_area_11_values,
    'Side of Spinal Cord': all_area_11_sides
}
PlottingModule.plot_area_dataframe(data15, directory, 'Tail Pinch')#'VF11')

#plotting delay vf11
all_11_delay_values = np.concatenate([
    delay_11_left_l, 
    delay_11_left_r, 
    delay_11_right_l, 
    delay_11_right_r
])

all_delay_11_sides = PlottingModule.plot_sides(delay_11_left_l, delay_11_left_r, delay_11_right_l, delay_11_right_r)
data16 = {
    'value' : all_11_delay_values, 
    'Side of Spinal Cord': all_delay_11_sides
}
PlottingModule.plot_delay_dataframe(data16, directory, 'Tail Pinch') #'VF11')


#Save data to csvs
