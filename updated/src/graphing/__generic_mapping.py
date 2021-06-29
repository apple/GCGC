def __generic_plotting(xdata_list, ydata_list, axs=None, colors=[], labels=[], plotting_function=None, optional=None):
    if not xdata_list:
        print("No timedata list in function plot_bar_compare()")
        return
    if not ydata_list:
        print("No heightdata list in plot_bar_compare()")
        return
    if not labels:
        print("No label list in plot_bar_compare()")
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

    # Apply the specific plotting
    for i in range(len(xdata_list)):
        plotting_function(xdata_list[i], ydata_list[i], axs, colors[i], labels[i], optional)
    return axs


# Creates a string in exactly the specified numchars.
# If len(string) > numchars, some of the string is not displayed.
# if len(string) < numchars, spaces are appended to the back of the string.
# returns a string containing the update string with len = numchars.
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
