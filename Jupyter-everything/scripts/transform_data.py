# transform_data.py
""" Take data and selectively return or parse sections of the data.
    Remove extra characters or add them. Does not change any values"""
# Ellis Brown
# 6/15/2021
import pandas as pd  # implicit. TODO: check if this is needed

# Access a Pandas dataframe constructed through parse_data.py with labeled columns.
# Return the timestamps and pauses as a list
def get_combined_xy_pauses(dataframe):
    if dataframe.empty:
        print("Warning: Empty dataframe")
        return [], []
    else:
        time_in_seconds = dataframe["TimeFromStart_seconds"]
        pauses_in_ms = dataframe["PauseDuration_miliseconds"]
        return time_in_seconds, pauses_in_ms


def remove_last_character(line):
    return line[:-1]


def get_time_in_seconds(dataframe):
    if dataframe.empty:
        return []
    else:
        return dataframe["TimeFromStart_seconds"]


def get_pauses_in_miliseconds(dataframe):
    if dataframe.empty:
        return []
    else:
        return dataframe["PauseDuration_miliseconds"]
