#       filter_and_group.py
#   
#   Given a set of filters, and groupings, take data from pandas dataframes, 
#   and return a modified subset of the data that follows the passed filters/groups.
#
# Ellis Brown
# 7-12-2021
#
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
    column="Duration_milliseconds",  # the column name that we are analyzing from our dataset
    colors=None, # a list colors. If none are provided, determinsitic colors returned for dataset
    column_timing = None # Overrides the timing column to collect, if provided. All values in the column must be ints/floats
):
    # Apply the filters, if any
    if filter_by:
        datasets = apply_filter(datasets, filter_by)       
    # Create the labels if non provided
    if not labels:
        labels = [str(num + 1) for num in range(len(datasets))]
    if not column_timing:
        column_timing = "TimeFromStart_seconds"
    # Group into lists of X/Y associated data with labels.
    timestamp_groups = [] # For time of event 
    datapoint_groups = [] # For data in 'column'
    group_labels = []     # Label to descrbe the group.
    
    if group_by:
        timestamp_groups, datapoint_groups, group_labels = arrange_into_groups(datasets, group_by, column, column_timing, labels)
    else:
        timestamp_groups, datapoint_groups, group_labels = arrange_no_groups(datasets, column, column_timing, labels)
     
    # Add the colors.
    if not colors:
        colors, alphas = get_colors_and_alphas(len(group_labels))
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
            
            # Apply functions return a boolean. Only retain rows that evaluate to True
            dfs[i] = dfs[i][dfs[i].apply(filter_by, axis=1)]
    
    else:
        # Return the same data if no filters needed
        dfs = datasets
    return dfs

#       get_colors_and_alphas
#
#   Given then number of colors, returns that many colors from a preset
#   sequence of repeating colors, begging at the start of the sequence
#
def get_colors_and_alphas(number_of_colors):
    preset_colors = [(230/255, 25/255, 75/255),
                    (60/255, 180/255, 75/255),
                    (215/255, 215/255, 25/255),
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
    while number_of_colors > len(preset_colors): # In the case where we need MANY colors, copy the cycle and add more.
        preset_colors = preset_colors + preset_colors

    for idx in range(number_of_colors):
        colors.append(preset_colors[idx])
        alphas.append(1)
    return colors, alphas

#       arrange_into_groups
#
#   Given a grouping pattern, and set of filtered datasets, creates a list of
#   X and Y datalists for each group found in the passed dataset.
#
def arrange_into_groups(datasets, group_by, column, column_timing, labels):
        timestamp_groups = []
        datapoint_groups = []
        group_labels = []
        for idx, df in enumerate(datasets): # Loop through all provided log datasets
            if not df.empty:
                if group_by not in df:
                    print("Warning: group_by group " + str(group_by) + " column not in dataset with columns " + str(df.columns))
                elif column not in df:
                    print("Warning: column \"" + str(column) + "\" not in dataset with columns " + str(df.columns))
                elif column_timing not in df:
                    print("Warning: column_timing \"" + str(column_timing) + "\" not in dataset with columns " + str(df.columns))
                else: 
                    # A non-empty df contains both X and Y columns.                    
                    
                    groups = {} # Create a dictionary to hold unique groups
                    if column_timing == "DateTime":
                        timing = pd.Series(matplotlib.dates.date2num(df[column_timing]))
                    else:
                        timing = df[column_timing]                        
                    for group, time, datapoint in zip(df[group_by], timing, df[column]):
                        if not group:
                            group = "( " + str(group_by) + " = None )" # None groups should all be put together
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
                        timestamp_groups.append(pd.Series(groups[key][0]))
                        datapoint_groups.append(pd.Series(groups[key][1]))
                        group_labels.append(groups[key][2])
                        
                    
        return timestamp_groups, datapoint_groups, group_labels
    
#       arrange_no_groups
#
#   Given no grouping pattern, take data from datasets, place them
#   into of X and Y datasets.
#
def arrange_no_groups(datasets, column, column_timing, labels):
    timestamp_groups = []
    datapoint_groups = []
    group_labels = [] # Included in case no data is extracted from a df
    for idx, df in enumerate(datasets):
        # Make sure both the columns are present, and rows are present
        if not df.empty and column_timing in df and column in df:
            if column_timing == "DateTime":
                timestamp_groups.append(pd.Series(matplotlib.dates.date2num(df[column_timing])))
            else:
                timestamp_groups.append(df[column_timing])
            datapoint_groups.append(df[column])
            group_labels.append(labels[idx])
                
    return timestamp_groups, datapoint_groups, group_labels
