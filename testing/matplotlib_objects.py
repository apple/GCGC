from matplotlib import pyplot as plt
import pl as pl
import random as r 
plt.rcParams['figure.figsize'] = [12, 7]
def main():
    fig, ax = plt.subplots()
    
    
    colors = ["g", "r", "b", "y"]
    for i in range(4):
        ax = plot_pauses(generate_random_table(3), ax, colors[i], label = str(i))
    ax = addLabels(ax)
    plt.show()

def someFunction(ax, c):
    ax.plot([20 * r.randint(2, 20) for x in range(r.randint(4,8))], color = c)
    return ax 

def addLabels(ax):
    ax.set_xlabel("X LABEL")
    ax.set_ylabel("Y LABEL")
    ax.set_title("the coolest")
    ax.legend()
    return ax 

def plot_pauses(table, ax, color = "", label = ""):
    
    ########################### setup ######################
    if not table:
        print("No table passed as a parameter. Abort.")
        return
    # Tables may/may not come with datetime information appended.
    # This information is not currently used. Therefore, shift past it
    if (len(table) == 5):
        shift = 0
    elif len(table) == 6:
        shift = 1
    else:
        print("Table length does not match expected.")
        print("Expected num cols: 5 or 6. Recieved: ", len(table))
        return
    
    timestamps = table[0 + shift]       # get timestamps from table information
    #timestamps = list(map(__time_to_float, timestamps)) # clean data 

    pause_information = table[-1]       # get pause information duration
    
    ## Create data set that mimimics an up and down line graph based on pause time.
    x_data = []
    y_data = []

    ###### Create X-Y Data. bumps for height based on pause duration #####
    for x,y in zip(timestamps, pause_information):
        # first, create a point at time before pause
        x_data.append(x)
        y_data.append(0)

        # next, create a point of y height, at that initial time
        x_data.append(x)
        y_data.append(y)

        # last point in pause duration high
        x_data.append(x + y)
        y_data.append(y)

        # end pause duration high
        x_data.append(x + y)
        y_data.append(0)
    
    # Plot the data created for this table. #
    ax.plot(x_data, y_data, color = color, label = label),    
    # return the subplot updated with the new information
    return ax


# Removes trailing 's' character from time in seconds
def __time_to_float(time):
    return float(time[:-1])

    
def generate_random_table(entry_count):
    entry_count += r.randint(0,5)
    table = [[x * r.randint(20,50) for x in range(entry_count)], [], [], [], [y * r.randint(0,10) for y in range(entry_count)]]
    return table

main()


