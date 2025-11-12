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

def count_partial_eth(word_list, partial_word):
  '''function tot figure out how many ethograms scored for each trial
        inputs: work_list = dataframe column names as list, patrial_word = Ethogram'''
  count = 0
  for word in word_list:
    if partial_word in word:
        count += 1
  return count



def excel_loop_dff(traces_folder, withdrawal_score, df1, stim_score, etho,conversion,conversion2, count):
    '''excel_loop function Loops through all the traces folder event excel sheets and saves df/f plots correlated to behaviors scored
    inputs: path to traces, user inputted withdrawal score, loaded behavior dataframe, user unputted stimulus and ethogram score, conversion and count indicated number of ethograms for the trial'''
    # Initialize an empty list to store DataFrames
    data_frames = []
    left_foot = ''
    right_foot = ''

    csv_files = [f for f in os.listdir(traces_folder) if f.endswith('.csv')]


    match = re.search(r'\d+', traces_folder)
    
    if match:
       num = int(match.group())
       title = num
       index = num-1
       #index doesn't work if there is duplicate rows
           
    #print(index)

    # Loop through the list of CSV files and read each into a DataFrame
    for file in csv_files:
        file_path = os.path.join(traces_folder, file)
        df = pd.read_csv(file_path)
        df['file'] = file
       #print(file)

          # Extract the file name without the extension
        #event_name = os.path.splitext(file)[0]
        #print(event_name)

         # Filter based on withdrawal score if applicable
        if withdrawal_score != 'N' and float(df1['W score'].iloc[index]) != float(withdrawal_score):
            print(f"Skipping Event {file} due to withdrawal score not equal to input")
            continue

        # Filter based on stimulus score if specified
        if stim_score != 'N' and float(df1['Stim score'].iloc[index]) != float(stim_score):
            print(f"Skipping Event {file} due to stimulus score not equal to input")
            continue

        data_frames.append(df)

    for i, data in enumerate(data_frames):
        full_name = data.iloc[0,2]
        event_name = full_name.split('_')[1].split('.')[0]
        
        x = sns.lineplot(data=data[['dff']], dashes=False)
    
    
        #get which foot stimulated
        
        foot = df1['Leg'].iloc[index]
        data = df1['Data'].iloc[index]
        stim = df1['Stimulus'].iloc[index]

        # might have to adjust this based on the framerate
        scale = conversion2/conversion # imaging FR/Behavior FR
        
        formatted_data = f'data{str(data).zfill(2)}'

        if stim == 'B':
            stimulus = 'Brush'
        elif stim == 5:
            stimulus = 'VF 5'
        elif stim == 8:
            stimulus = 'VF 8'
        else:
            #stimulus = 'VF 11'
            stimulus = 'Tail Pinch'

      # Append to the list only if the data is not already in the list
        if foot == 'R':
            foot_stim = 'Right'
            #if formatted_data not in right_foot:
                #right_foot.append(formatted_data)
            right_foot = formatted_data
        else:
            foot_stim = 'Left'
            #if formatted_data not in left_foot:
            #left_foot.append(formatted_data)
            left_foot = formatted_data
       

        #Plotting df/f
        x.set(xlabel="Frame", ylabel="dF/F", title=f'{stimulus} {event_name} Stimulated {foot_stim} Foot')
        # Plot line for stimulus `Onset`
        line = df1['Onset'].iloc[index]
        scaled_stim_onset = line*scale
        x.axvline(x=scaled_stim_onset, color="black", linestyle="--", label="Stimulus Onset")

        ethogram_id = [chr(97+i) for i in range(count)]
         # Plot line for `Onset_ethogram` if it exists
        for e in ethogram_id:
            onset_col = f'Onset_e{e}'
            offset_col = f'Offset_e{e}'
            ethogram_col = f'Ethogram_{e}'
            #print(ethogram_col)
            
            if etho != 'N' and not pd.isna(df1[onset_col].iloc[index]):
                line2 = df1[onset_col].iloc[index] * scale
                line2_0 = df1[offset_col].iloc[index]* scale
                if df1[ethogram_col].iloc[index] == 1:
                    label = 'Forepaw Licking/Grooming'
                    color = 'red'
                elif df1[ethogram_col].iloc[index] == 2:
                    label = 'Rearing'
                    color = 'purple'
                elif df1[ethogram_col].iloc[index] == 3:
                    label = 'Hindlimb/Body Grooming'
                    color='green'
                elif df1[ethogram_col].iloc[index] == 4:
                    label = 'Walk/move in small circle'
                    color = '#CC9900'
                elif df1[ethogram_col].iloc[index] == 5:
                    label = 'Walk/move in large circle'
                    color = 'magenta'
                elif df1[ethogram_col].iloc[index] == 6:
                    label = 'Stick nose through grate'
                    color = 'cyan'
                elif df1[ethogram_col].iloc[index] == 7:
                    label = 'Guarding'
                    color = 'black'
                #just added this check if errors script
                # elif str(df[ethogram_col].iloc[index].strip()) == 'S':
                #     label = 'Lifting of foot correlated to stimulus'
                #     color = 'blue'  
                else:
                    label = 'Hindleg passively flexed with force of stimulus'
                    color = '#00FF00'
                    


                # Add shaded region between behavior line (onset) and line_off (offset)
                plt.fill_between([line2, line2_0], -0.05, 0.2, color=color, alpha=0.3, label=label)
                

    # Add legend, y-axis limits, and display the plot
        plt.legend(loc='upper right', fontsize='small')
        plt.ylim(-0.05, 0.2)


        # Save the plot
        # Define folder based on foot stimulation
        save_folder = os.path.join(traces_folder, 'Right Foot Stimulated' if foot_stim == 'Right' else 'Left Foot Stimulated')
        
        # Create directory folder if it does not exist
        os.makedirs(save_folder, exist_ok=True)
        #print(title, foot_stim)

        plot_file_path = os.path.join(save_folder, f'Data{title}dff_plot{event_name}.png')
        plt.savefig(plot_file_path)
        plt.close()



    return left_foot, right_foot


    
