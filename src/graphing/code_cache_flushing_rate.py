from src.filter_and_group import get_colors_and_alphas
from matplotlib import pyplot as plt

#       calculate_code_cache_flushing_rate
#
#   Returns a plot object for the code cache flushing rate
#
def calculate_code_cache_flushing_rate(
    gc_event_dataframes,  # List of dataframes, containing gc event information
    labels=None,  # List of strings to describe each gc_event_dataframe
    colors=None,  # Colors to override
    plot=None,  # Matplotlib axes to plot onto. If none is provided, one is created
    line_graph=False  # Plots as a line graph rather than a scatter plot
):
    if len(gc_event_dataframes) > len(labels):
        print("Not enough labels to plot")

    rates_to_plot = []
    rates_timestamps_to_plot = []
    labels_to_plot = []

    for index in range(len(gc_event_dataframes)):
        rates, rates_timestamps = get_rates_with_timestamps(gc_event_dataframes[index])

        if len(rates) > 0:
            rates_to_plot.append(rates)
            rates_timestamps_to_plot.append(rates_timestamps)
            labels_to_plot.append(labels[index])

    if colors is None:
        colors, _ = get_colors_and_alphas(len(rates_to_plot))
    elif len(rates_to_plot) > len(colors):
        print("Not enough colors to plot")

    # If no plot is passed in, then create a new plot
    if plot is None:
        f, plot = plt.subplots()

    # Plot the data
    for rates, rates_timestamps, label, color in zip(rates_to_plot, rates_timestamps_to_plot, labels_to_plot, colors):
        if line_graph:
            plot.plot(rates_timestamps, rates, label=label, color=color)
        else:
            plot.scatter(rates_timestamps, rates, label=label, color=color)

    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    return plot


#       get_rates_with_timestamps
#
#   Calculates and returns the code cache flushing rates and their corresponding timestamps.
#
#   The flushing rate can generally be calculated by: 1 / time delta (i.e., time difference between consecutive
#   flushes). But since there is the possibility of more than one event having the same timestamp (e.g., when a
#   dataframe is generated from a group of files), a time delta of zero causes a division by zero error (1 / 0).
#   Therefore, the flushing rate is calculated by:
#   (number of flushes that occurred at a specific timestamp) / (time difference from previous non-equal timestamp).
#
def get_rates_with_timestamps(gc_event_dataframe):
    code_cache_flushing_column = gc_event_dataframe["CodeCacheFlushing"]
    time_from_start_column = gc_event_dataframe["TimeFromStart_seconds"]

    rates = []
    rates_timestamps = []

    number_of_flushes = 0
    previous_time_from_start = 0  # 0 seconds: beginning of program runtime

    for index in range(len(code_cache_flushing_column)):
        if code_cache_flushing_column.iloc[index] is not None:
            number_of_flushes += 1
            current_time_from_start = time_from_start_column.iloc[index]
            time_delta = current_time_from_start - previous_time_from_start

            if time_delta > 0:
                rates.append(number_of_flushes / time_delta)
                rates_timestamps.append(current_time_from_start)

                number_of_flushes = 0
                previous_time_from_start = current_time_from_start

    return rates, rates_timestamps
