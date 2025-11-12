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
import left_rightModule


def flatten(list):
    '''Takes in a list and flattens dataframe series to just numerical values to use for plotting'''
    list = [val for series in list for val in series.values]
    return list



def plot_percent(var_list, directory, stimulus):
    '''Plots percent responding to stimulus as barplot'''
    variable_names = ['Ipsi, Injured Foot', 'Contra, Injured Foot', 'Ipsi, Uninjured Foot', 'Contra, Uninjured Foot']
    plt.figure(figsize = (10, 6))
    plt.bar(variable_names, var_list, edgecolor = 'black', facecolor = 'green')
    plt.axvline(x =1.5, color = 'gray', linestyle = '--', linewidth =1)
    plt.ylim(0,100)

    plt.xlabel('Side of Spinal Cord', labelpad = 30)
    plt.ylabel("Percent Responding")
    plt.title(f'Percent of Trials Responding to {stimulus}')
    # Save the percent  plot
    plot_file_path_box1= os.path.join(directory, f'boxplot_percent_{stimulus}.png')
    plot_file2 = os.path.join(directory, f'boxplot_percent_{stimulus}.eps')
    plt.savefig(plot_file2)
    plt.savefig(plot_file_path_box1)

    # Create a DataFrame
    df = pd.DataFrame({'Side of Spinal Cord': variable_names, 'Percent Responding': var_list})

    # Define the CSV save path
    csv_file_path = os.path.join(directory, f'percent_respond_{stimulus}.csv')

    # Save the data as CSV
    df.to_csv(csv_file_path, index=False)
  
    plt.close()

    

def left_right_list_sort(list):
    '''Function takes in a list to iterate over and apply l_analysis() function
    returns 4 differents lists containing different parameters to plot'''
    delay= []
    duration = []
    area = []
    dff = []

    for i in list:
        e, m, d, a, de = left_rightModule.l_analysis(i)
        dff.append(m)
        duration.append(d)
        delay.append(de)
        area.append(a)
    

    return delay, duration, area, dff

def plot_sides(left, right, rl, rr):
    '''set up categories for plotting based on foot stimulated and side of spinal cord responding '''
    all_sides = (
        ['ipsi, injured foot'] * len(left) +
        ['contra, injured foot  '] * len(right) +
        ['ipsi, uninjured foot'] * len(rl) +
        ['contra, uninjured foot'] * len(rr)
    )

    return all_sides

def plot_dff_dataframe (df, directory, stimulus):
    '''Takes in a dataframe for plotting and export as png and eps'''
    
    plot_df1 = pd.DataFrame(df)

    if plot_df1.empty:
        plot_df1=pd.DataFrame({'value': [0], 'Side of Spinal Cord':['No Data']})
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Side of Spinal Cord', y='value', data=plot_df1, width=0.2, boxprops=dict(facecolor = 'none', edgecolor='black'))

    # Create the swarmplot
    sns.swarmplot(x='Side of Spinal Cord', y='value', data=plot_df1, color='black', alpha=0.5)
    # Add a dotted line between the "left" and "right" categories
    plt.axvline(x=1.5, color='gray', linestyle='--', linewidth=1)

    # Set labels
    plt.xlabel("Side of Spinal Cord", labelpad=20)
    plt.ylabel('Max DF/F')
    plt.title(f'{stimulus} Max DF/F Per Event')

    # Save the duration  plot
    plot_file_path_box = os.path.join(directory, f'boxplot_dff_{stimulus}.png')
    plot_file1 = os.path.join(directory, f'boxplot_dff_{stimulus}.eps')
    plt.savefig(plot_file1)
    plt.savefig(plot_file_path_box)
    csv_path = os.path.join(directory,f"{stimulus}dff.csv")
    plot_df1.to_csv(csv_path, index=False)
    plt.close()

def plot_dur_dataframe (df, directory, stimulus):
    '''Takes in a dataframe, directory to save and stimulus given for plotting duration boxplot and export as png and eps'''
    
    plot_df1 = pd.DataFrame(df)

    if plot_df1.empty:
        plot_df1=pd.DataFrame({'value': [0], 'Side of Spinal Cord':['No Data']})
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Side of Spinal Cord', y='value', data=plot_df1, width=0.2, boxprops=dict(facecolor = 'none', edgecolor='black'))

    # Create the swarmplot
    sns.swarmplot(x='Side of Spinal Cord', y='value', data=plot_df1, color='black', alpha=0.5)
    # Add a dotted line between the "left" and "right" categories
    plt.axvline(x=1.5, color='gray', linestyle='--', linewidth=1)

    # Set labels
    plt.xlabel("Side of Spinal Cord", labelpad=20)
    plt.ylabel('Duration (s)')
    plt.title(f'{stimulus} Duration Per Event')

    # Save the dff brush plot
    plot_file_path_box = os.path.join(directory, f'boxplot_duration_{stimulus}.png')
    plot_file1 = os.path.join(directory, f'boxplot_duration_{stimulus}.eps')
    plt.savefig(plot_file1)
    plt.savefig(plot_file_path_box)
    csv_path = os.path.join(directory,f"{stimulus}duration.csv")
    plot_df1.to_csv(csv_path, index=False)
    plt.close()

def plot_area_dataframe(df, directory, stimulus):
    '''Takes in a dataframe, directory to save and stimulus given and plots area boxplot and exports as eps and png'''
    plot_df1 = pd.DataFrame(df)

    if plot_df1.empty:
        plot_df1=pd.DataFrame({'value': [0], 'Side of Spinal Cord':['No Data']})
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Side of Spinal Cord', y='value', data=plot_df1, width=0.2, boxprops=dict(facecolor = 'none', edgecolor='black'))

    # Create the swarmplot
    sns.swarmplot(x='Side of Spinal Cord', y='value', data=plot_df1, color='black', alpha=0.5)
    # Add a dotted line between the "left" and "right" categories
    plt.axvline(x=1.5, color='gray', linestyle='--', linewidth=1)

    # Set labels
    plt.xlabel("Side of Spinal Cord", labelpad=20)
    plt.ylabel('Normalized Area (%)')
    plt.title(f'{stimulus} Normalized Area Per Event')

    # Save the area plot
    plot_file_path_box = os.path.join(directory, f'boxplot_area_{stimulus}.png')
    plot_file1 = os.path.join(directory, f'boxplot_area_{stimulus}.eps')
    plt.savefig(plot_file1)
    plt.savefig(plot_file_path_box)
    csv_path = os.path.join(directory,f"{stimulus}area.csv")
    plot_df1.to_csv(csv_path, index=False)
    plt.close()

def plot_delay_dataframe(df, directory, stimulus):
    '''Takes in a dataframe, directory to save and stimulus given and plots delay boxplot and exports as eps and png'''
    plot_df1 = pd.DataFrame(df)

    if plot_df1.empty:
        plot_df1=pd.DataFrame({'value': [0], 'Side of Spinal Cord':['No Data']})
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Side of Spinal Cord', y='value', data=plot_df1, width=0.2, boxprops=dict(facecolor = 'none', edgecolor='black'))

    # Create the swarmplot
    sns.swarmplot(x='Side of Spinal Cord', y='value', data=plot_df1, color='black', alpha=0.5)
    # Add a dotted line between the "left" and "right" categories
    plt.axvline(x=1.5, color='gray', linestyle='--', linewidth=1)

    # Set labels
    plt.xlabel("Side of Spinal Cord", labelpad=20)
    plt.ylabel('Delay (s)')
    plt.title(f'{stimulus} Delay Per Event')

    # Save the area plot
    plot_file_path_box = os.path.join(directory, f'boxplot_delay_{stimulus}.png')
    plot_file1 = os.path.join(directory, f'boxplot_delay_{stimulus}.eps')
    plt.savefig(plot_file1)
    plt.savefig(plot_file_path_box)
    csv_path = os.path.join(directory,f"{stimulus}delay.csv")
    plot_df1.to_csv(csv_path, index=False)
    
    plt.close()