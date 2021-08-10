#       percentiles.py
#
#   Analyzes trends in lists of pause data, and prints percentiles
#   of the longest paused time
#
#   Ellis Brown, 6/29/2021



import numpy as np

#       print_percentiles
#
#   Display what percent of pauses meet a certain percentile threshold
#
def print_percentiles(pauses_miliseconds=[], print_title=True, percentiles=None, label=None):
    # Parameters:
    #   pauses_miliseconds  : a list of pauses to be analyzed (in any order)
    #   print_title         : True if you would like column headers
    #   percentiles         : a list of percentiles to be plotted, in float list form.
    #   label               : a label to be printed. Should be 0-10 characters
    if type(pauses_miliseconds) != type(None):
        pauses_miliseconds = list(pauses_miliseconds)
    if not pauses_miliseconds:
        return
    pauses_miliseconds = sorted(pauses_miliseconds, reverse=True)

    percentile_table = {}
    if not percentiles:
        percentiles = [50, 95, 99, 99.99]
    for p in percentiles:
        percentile_table[p] = np.percentile(pauses_miliseconds, p)
    if not label:
        label = "label"
    num_column_spaces = 18
    if print_title:
        title = ""
        for p in percentiles:
            title += __string_const_chars(str(p) + "%", num_column_spaces) + " | "
        print("    | " + title + "\n" + "-" * (len(title) + 12))
    print(__string_const_chars(label, 3) + " | ", end="")
    
    for p in percentiles:
        print(float_constant_chars(str(round(percentile_table[p], 4)), num_column_spaces) + " | ", end="")
    print("")


#       compare_pauses_percentiles
#
#   Plot the percentiles for pause time in miliseconds for all lists provided, on the same table
#   Parameters:
#       pauses_miliseconds    : list of [list of pauses as floats in ms]
#       percentiles(optional) : list of float value percentiles to be viewed.
#
def compare_pauses_percentiles(list_of_list_pauses_ms=[], percentiles=None, labels=None):
    if not list_of_list_pauses_ms:
        print("No list_of_list_pauses_ms provided to plot_compare_percentiles")
        return
    if not labels:
        labels = [str(i) for i in range(len(list_of_list_pauses_ms))]
    print_percentiles(list_of_list_pauses_ms[0], True, percentiles, labels[0])

    for i in range(1, len(list_of_list_pauses_ms)):
        print_percentiles(list_of_list_pauses_ms[i], False, percentiles, labels[i])



#       __string_const_chars
#
#   Creates a string in exactly the specified numchars.
#   If len(string) > numchars, some of the string is not displayed.
#   if len(string) < numchars, spaces are appended to the back of the string.
#   returns a string containing the update string with len = numchars.
#
def __string_const_chars(string, numchars):
    string = str(string)
    char_list = ""
    for i in range(len(string)):
        char_list += string[i]
        numchars -= 1
        if numchars == 0:
            return char_list
    temp_list = ""
    for i in range(numchars):
        temp_list += " "
    return temp_list + char_list

from src.graphing.trends import float_constant_chars
