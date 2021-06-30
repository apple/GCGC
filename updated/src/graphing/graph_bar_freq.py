# fig, ax = plt.subplots()
# labels = [str(i * bucket_size_ms) for i in range(1, len(buckets) + 1)]
# print(labels)
# ax.bar(labels, height=buckets, align="center")
# ax.set_xlabel("Miliseconds groupings")
# ax.set_ylabel("Pause count")
# _ = ax.set_title("Frequencies of STW pauses in miliseconds")

# # fig.autofmt_xdate() #
# # Turn on if labels are crossing over each other
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal


def compare_frequencies_bar(buckets, bucket_size_ms, legend):
    # assert parameters

    # create plot form data
    fig, ax = plt.subplots()
    colors = ["cyan", "green", "blue", "purple", "pink", "k"]
    xlabels = [str(i * bucket_size_ms) for i in range(1, len(buckets) + 1)]
    width = 0.8 / len(buckets)
    max_x_coordinate = 0
    for idx in range(len(buckets)):

        x_coordinates = list(np.arange(len(buckets[idx])) + width * idx)
        max_x_coordinate = int(max(max_x_coordinate, len(x_coordinates)))
        ax.bar(x_coordinates, buckets[idx], width, label=legend[idx], color=colors[idx])

    # width * len(buckets) / 2 is the middle of the bars.
    # width / 2 is the middle of the individual center bar
    ax.set_xticks(np.arange(max_x_coordinate) + ((width * len(buckets) / 2) - width / 2))
    # Set the values to show frequencies. Use Decimal class to stop rounding errors.
    ax.set_xticklabels(
        [
            Decimal(str(bucket_size_ms)) * Decimal(str(val)) + Decimal(str(bucket_size_ms))
            for val in np.arange(max_x_coordinate)
        ]
    )
    ax.set_xlabel("Time paused in miliseconds bucket")
    ax.set_ylabel("Frequency during runtime")
    ax.set_title("Frequencies of pauses during runtime")
    ax.legend()
    ax.grid()
