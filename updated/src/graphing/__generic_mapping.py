#       __generic_mapping.py
#
#   Helper functions to help plotting with parameter checking more easily, and printing ASCII table format.
#
#   Ellis Brown
#   June 2021

import matplotlib.pyplot as plt
import matplotlib

#       __generic_plotting
#
#   Given a plotting function, and the parameters to that plotting function, carefully comapres the parameters for that
#   function, and prints descriptive error messages when parameters are incorrect.
#
def __generic_plotting(xdata_list, ydata_list, axs=None, colors=[], labels=[], plotting_function=None, optional=None):
    if not xdata_list:
        print("No xdata_list list in function __generic_plotting()")
        return
    if not ydata_list:
        print("No ydata_list list in __generic_plotting()")
        return
    if not labels:
        print("No labels list in __generic_plotting()")
    if len(xdata_list) != len(ydata_list):
        print("Length of xdata_lists and ydata_lists do not match.", end="")
        print("xdata_lists: " + str(len(xdata_list)) + ", ydata_list: " + str(len(ydata_list)))
        return
    if len(xdata_list) != len(labels):
        print("Length of xdata_lists and labels do not match. ", end="")
        print("xdata_lists: " + str(len(xdata_list)) + ", labels: " + str(len(labels)))
        print(labels)
        return
    if not colors:
        colors = []
    while len(colors) < len(xdata_list):
        colors.append(None)
    if not axs:
        fig, axs = plt.subplots()
    # Confirm datatypes
    assert isinstance(xdata_list, list)
    assert isinstance(ydata_list, list)
    assert isinstance(colors, list)
    assert isinstance(labels, list)
    # Apply the specific plotting
    for i in range(len(xdata_list)):
        plotting_function(xdata_list[i], ydata_list[i], axs, colors[i], labels[i], optional)
    return axs


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
