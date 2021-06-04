import numpy as np
import matplotlib
import matplotlib.pyplot as plt

vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
              "potato", "wheat", "barley"]
farmers = ["Farmer Joe", "Upland Bros.", "Smith Gardening",
           "Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]

harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                    [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
                    [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
                    [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
                    [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
                    [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                    [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])
print(type(harvest))

fig, ax = plt.subplots()
im = ax.imshow(harvest)

# We want to show all ticks...
ax.set_xticks(np.arange(len(farmers)))
ax.set_yticks(np.arange(len(vegetables)))
# ... and label them with the respective list entries
ax.set_xticklabels(farmers)
ax.set_yticklabels(vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")

ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.show()

# table = [ [] , [] , [] , [] ]
# def __time_from_float(time):
#     return float(time[:-1])


# def get_heapmap(table):
#     shift = __getShift(table)
#     timestamps = table[0 + shift]
#     timestamps = map(__time_from_float, timestamps)  # clean data.
#     pauses     = table[-1]
#     num_b = 10 # constant param
#     x_b = [[] for i in range(num_b)]
#     max_time             = timestamps[-1]
#     bucket_time_duration = max_time / num_b

#     # populate buckets along the x axis.
#     for pause, time in zip(pauses, timestamps):
#         bucket_no = time / bucket_time_duration
#         if bucket_no >= num_b:
#             bucket_no = num_b - 1
#         x_b[bucket_no].append(time)

#     # calculate the max & min time in any time.
#     max_pause = max(pauses)
#     min_pause = min(pauses)

#     bucket_pause_duration = (max_pause - min_pause) / num_b
#     heapmap = []
#     for bucket in x_b:
#         yb = [0 for i in range(num_b)]
#         for time in bucket:
#             y_bucket_no = (time - min_pause) / num_b
#             if y_bucket_no >= num_b:
#                 y_bucket_no = num_b - 1
#             yb[y_bucket_no] += 1
#         heapmap.append(yb)

#     return heapmap, min_pause, max_pause, max_time # all data needed to plot a heatmap.
# VALID HEAT MAP COLORS BELOW
"""'YlOrRe' is not a valid value for name; supported values are 'Accent', 'Accent_r', 
'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 
'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens',
'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r',
'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 
'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r',
'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 
'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 
'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 
'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 
'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r',
'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone',
'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 
'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 
'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 
'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 
'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg',
'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 
'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 
'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r',
'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', '
prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 
'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r',
'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r',
'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted',
'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'"""


# Fix the small heat map problem with data (???)
# Create sample test data, and then input it and verify outputs.
def generateTable(dimensions):
    table = [[], [], [], [], []]
    for i in range(200):
        table[0].append(i)
        table[-1].append(i)
    return table
        

def __get_heatmap(table, num_b):
    shift = __getShift(table)
    timestamps = table[0 + shift]
    timestamps = list(map(__time_to_float, timestamps))  # clean data.
    pauses     = table[-1]
    x_b = [[] for i in range(num_b)]
    max_time             = timestamps[-1]
    bucket_time_duration = max_time / num_b

    # populate buckets along the x axis.
    for pause, time in zip(pauses, timestamps):
        bucket_no = int(time / bucket_time_duration)
        if bucket_no >= num_b:
            bucket_no = num_b - 1
        x_b[bucket_no].append(pause)

    # calculate the max & min time in any time.
    max_pause = max(pauses)
    min_pause = min(pauses)
    print("MAX PAUSE", max_pause)
    print("MIN PAUSE", min_pause)

    bucket_pause_duration = (max_pause - min_pause) / num_b
    heatmap = []
    for bucket in x_b:
        yb = [0 for i in range(num_b)]
        for time in bucket:
            y_bucket_no = int((time - min_pause) / bucket_pause_duration)
            if y_bucket_no >= num_b:
                y_bucket_no = num_b - 1
            yb[y_bucket_no] += 1
       
        heatmap.append(yb[::-1]) # reverse so they enter the list correct order.
        heatmap = heatmap[::-1]
    return heatmap, min_pause, max_pause, max_time # all data needed to plot a heatmap.