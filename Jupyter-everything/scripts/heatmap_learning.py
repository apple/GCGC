import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
#               "potato", "wheat", "barley"]
# farmers = ["Farmer Joe", "Upland Bros.", "Smith Gardening",
#            "Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]

# harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
#                     [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
#                     [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
#                     [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
#                     [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
#                     [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
#                     [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])
# print(type(harvest))

# fig, ax = plt.subplots()
# im = ax.imshow(harvest)

# # We want to show all ticks...
# ax.set_xticks(np.arange(len(farmers)))
# ax.set_yticks(np.arange(len(vegetables)))
# # ... and label them with the respective list entries
# ax.set_xticklabels(farmers)
# ax.set_yticklabels(vegetables)

# # Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#          rotation_mode="anchor")

# # Loop over data dimensions and create text annotations.
# for i in range(len(vegetables)):
#     for j in range(len(farmers)):
#         text = ax.text(j, i, harvest[i, j],
#                        ha="center", va="center", color="w")

# ax.set_title("Harvest of local farmers (in tons/year)")
# fig.tight_layout()
# plt.show()

table = [ [] , [] , [] , [] ]
def __time_from_float(time):
    return float(time[:-1])


def get_heapmap(table):
    shift = __getShift(table)
    timestamps = table[0 + shift]
    timestamps = map(__time_from_float, timestamps)  # clean data.
    pauses     = table[-1]
    num_b = 10 # constant param
    x_b = [[] for i in range(num_b)]
    max_time             = timestamps[-1]
    bucket_time_duration = max_time / num_b

    # populate buckets along the x axis.
    for pause, time in zip(pauses, timestamps):
        bucket_no = time / bucket_time_duration
        if bucket_no >= num_b:
            bucket_no = num_b - 1
        x_b[bucket_no].append(time)

    # calculate the max & min time in any time.
    max_pause = max(pauses)
    min_pause = min(pauses)

    bucket_pause_duration = (max_pause - min_pause) / num_b
    heapmap = []
    for bucket in x_b:
        yb = [0 for i in range(num_b)]
        for time in bucket:
            y_bucket_no = (time - min_pause) / num_b
            if y_bucket_no >= num_b:
                y_bucket_no = num_b - 1
            yb[y_bucket_no] += 1
        heapmap.append(yb)

    return heapmap
