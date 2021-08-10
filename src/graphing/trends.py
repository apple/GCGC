#       trends.py
#
#   Given a list of floats, analyze macro trends within the data such as
#   the sum, count, and max/min. Print using an ASCII table.
#
#   Ellis Brown, 6/29/2021

from os import times
import pandas as pd
import numpy as np

#       print_trends
#
# Print the trends within the data (total number of pauses, max wait, total wait mean wait)
# returns total wait
#
def print_trends(pauses_miliseconds, label=None, print_title=True, total_runtime_seconds=0, timestamps=None):
    # Parameters:
    #   pauses_miliseconds    : list of pauses (floats)
    #   label                 : label for this row in the table
    #   print_title(optional) : bool, True => print recorded values
    pauses_miliseconds = list(pauses_miliseconds)
    if type(timestamps) != type(None):
        timestamps = list(timestamps)
    if pauses_miliseconds:
        max_pause = round(max(pauses_miliseconds, key=lambda i: float(i)), 4)
        sum_pauses = round(sum(float(i) for i in pauses_miliseconds), 4)
        average_wait = round(sum_pauses / len(pauses_miliseconds), 4)
        std_deviation = round(np.std(pauses_miliseconds), 4)
    else:
        max_pause, sum_pauses, average_wait, std_deviation = 0, 0, 0, 0
    throughput = None
    if total_runtime_seconds:
        print(total_runtime_seconds)
        throughput = round(((total_runtime_seconds * 1000) - sum_pauses) / (total_runtime_seconds * 1000), 4) * 100
    elif timestamps:
        throughput = round(((timestamps[-1] * 1000) - sum_pauses) / (timestamps[-1] * 1000), 4) * 100

    # Print title with formatting
    if print_title:
        title = "  Trends (ms)   | "  # 15 + 3 characters
        title += "Event Count   | "
        title += "Max Duration  | "
        title += "Sum Duration  | "
        title += "Mean Duration | "
        title += "Std Dev.      |"
        if throughput:
            title += " Throughput    |"
        print(title)
        print("-" * len(title))
    num_chars = 13
    if not label:
        label = "Run:"
    # print with correct formatting the values
    number_label_chars = 15
    label = label[-number_label_chars:]
    line = __string_const_chars(label, number_label_chars) + " | "
    line += float_constant_chars(str(len(pauses_miliseconds)), num_chars) + " | "
    line += float_constant_chars(str(max_pause), num_chars) + " | "
    line += float_constant_chars(str(sum_pauses), num_chars) + " | "
    line += float_constant_chars(str(average_wait), num_chars) + " | "
    line += float_constant_chars(str(std_deviation), num_chars) + " | "
    if throughput:
        line += float_constant_chars(str(round(throughput, 7)), num_chars) + " % "
    print(line)

def float_constant_chars(value, length):
    value = float(value)
    output = "%9.4f" % (value)
    output_len = len(str(output))
    output = (length - output_len) * " " + output    
    return output


#       compare_trends
#
#   Compares trends from a list of pauses lists
#
def compare_trends(pauses_ms_lists, labels=None, lists_of_total_program_runtime=[], lists_of_timestamps=[]):
    assert isinstance(pauses_ms_lists, list)
    if not pauses_ms_lists:
        print("No pauses_ms_lists in compare_trends.")
        return
    if not labels:
        labels = [str(i) for i in range(len(pauses_ms_lists))]
    # The second and third parameters are optionally lists. Pass them if the parameter exists , and decide between the two.
    # Otherwise, pass none. Pass the first (index 0) with title TRUE, the rest in loop title FALSE.
    if lists_of_total_program_runtime:
        print_trends(pauses_ms_lists[0], labels[0], True, lists_of_total_program_runtime[0])
        for i in range(1, len(pauses_ms_lists)):
            print_trends(pauses_ms_lists[i], labels[i], False, lists_of_total_program_runtime[i])
    elif lists_of_timestamps:
        print_trends(pauses_ms_lists[0], labels[0], True, timestamps=lists_of_timestamps[0])
        for i in range(1, len(pauses_ms_lists)):
            print_trends(pauses_ms_lists[i], labels[i], False, timestamps=lists_of_timestamps[i])
    else:
        print_trends(pauses_ms_lists[0], labels[0], True)
        for i in range(1, len(pauses_ms_lists)):
            print_trends(pauses_ms_lists[i], labels[i], False)


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
    for i in range(numchars):
        char_list += " "
    return char_list
