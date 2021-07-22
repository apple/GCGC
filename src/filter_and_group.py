#       filter_and_group.py
#
# Ellis Brown
# 7-12-2021
#
import math
import matplotlib

#       filter_and_group
#
#   Given a list of datasets, use provided parameters to group and split
#   the data into useable pandas series. 
#
def filter_and_group(
    datasets,  # list of gc_event_dataframes
    group_by=None,  # creates a group for each unique value in a column specified 
    filter_by=None, # a function to be applied to the row of the table. Should return a boolean
    labels=None, # a list of strings to describe the datasets passed in 
    column="Duration_miliseconds",  # the column name that we are analyzing from our dataset
    colors=None, # a list colors. If none are provided, determinsitic colors returned for dataset
    column_timing = None # Overrides the timing column to collect, if provided. All values in the column must be ints/floats
):
    if filter_by:
        datasets = apply_filter(datasets, filter_by)
    if not labels:
        labels = [str(num + 1) for num in range(len(datasets))]

    # After verifying/setting paramets, loop through all datasets.
    timestamp_groups = [] # For time of event 
    datapoint_groups = [] # For data in 'column'
    group_labels = []
    log_number_list = [] # used to specify which dataset in original list
    if not column_timing:
        column_timing = "TimeFromStart_seconds"
    
    if group_by: # We need to create groups within each dataset
        
        for idx, df in enumerate(datasets):
            if not df.empty:
                if group_by not in df:
                    print("Warning: group_by group " + str(group_by) + " column not in dataset with columns " + str(df.columns))
                elif column not in df:
                    print("Warning: column \"" + str(column) + "\" not in dataset with columns " + str(df.columns))
                else:
                    if column_timing in df:
                        groups = {}
                        if column_timing == "DateTime":
                            timing = matplotlib.dates.date2num(df[column_timing])
                        else:
                            timing = df[column_timing]
                        for group, time, datapoint in zip(df[group_by], timing, df[column]):
                            if group:
                                if group not in groups:
                                    # Create a new group for each unique item
                                    groups[group] = [[], [], str(labels[idx]) + ": " + str(group)]
                                # add the datapoints and time, based on the grouping
                                
                                groups[group][0].append(time)
                                groups[group][1].append(datapoint)

                        # Sort keys so groups print in the same order between files
                        keys = list(groups.keys())
                        keys.sort()

                        for key in keys:
                            timestamp_groups.append(groups[key][0])
                            datapoint_groups.append(groups[key][1])
                            group_labels.append(groups[key][2])
                            log_number_list.append(idx)
                    else:
                        print("Warning: column_timing \"" + str(column_timing) + "\" not in dataset with columns " + str(df.columns))
                
    else: # no groups are required, just use the entire filtered dataset as a group 
        
        for idx, df in enumerate(datasets):
            if not df.empty:
                if column_timing in df:
                    if column in df:
                        if column_timing == "DateTime":
                            timestamp_groups.append(matplotlib.dates.date2num(df[column_timing]))
                        else:
                            timestamp_groups.append(df[column_timing])
                        datapoint_groups.append(df[column])
                        group_labels.append(labels[idx])
                        log_number_list.append(idx)
                        
    # Determine the colors from the dataset. If colors were passed, use those instead.  
    if not colors:
        colors, alphas = get_colors_and_alphas(log_number_list, group_by)
    else:
        alphas = [1 for i in range(len(colors))]

    return timestamp_groups, datapoint_groups, group_labels, colors, alphas

import pandas as pd
#       apply_filter
#
#   For each dataset, apply each filter. Create a copy of the data to be fitered,
#   so the original data is not modified or lost. Return the list of copied & filetered datasets
#
def apply_filter(datasets, filter_by=None):
    dfs = []
    if filter_by:
        # create a copy, to be modified
        for df in datasets:
            dfs.append(df.copy())

        # the reason to use index is to update the actual value
        for i in range(len(dfs)): 
            for boolean_function in filter_by:
                #  The boolean function returns true/false, and only keeps rows that evaluate to true
                dfs[i] = dfs[i][dfs[i].apply(boolean_function, axis=1)]
    else:
        dfs = datasets
    return dfs


def get_colors_and_alphas(log_no_list, group_by):
    prev_log_no = 0
    preset_colors = [(230/255, 25/255, 75/255),
                    (60/255, 180/255, 75/255),
                    (255/255, 225/255, 25/255),
                    (0/255, 130/255, 200/255),
                    (245/255, 130/255, 48/255),
                    (145/255, 30/255, 180/255),
                    (70/255, 240/255, 240/255),
                    (240/255, 50/255, 230/255),
                    (210/255, 245/255, 60/255),
                    (250/255, 190/255, 212/255),
                    (0/255, 128/255, 128/255),
                    (220/255, 190/255, 255/255),
                    (170/255, 110/255, 40/255),
                    (255/255, 250/255, 200/255),
                    (128/255, 0/255, 0/255),
                    (170/255, 255/255, 195/255),
                    (128/255, 128/255, 0/255),
                    (255/255, 215/255, 180/255),
                    (0/255, 0/255, 128/255),
                    (128/255, 128/255, 128/255),
                    (0, 0, 0)] # https://sashamaps.net/docs/resources/20-colors/
    colors = []
    alphas = []
    while len(log_no_list) > len(preset_colors):
        preset_colors = preset_colors + preset_colors
    for idx in range(len(log_no_list)):
        colors.append(preset_colors[idx])
        alphas.append(1)
    return colors, alphas
 