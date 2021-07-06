def apply_restrictions(
    datasets, group_by=None, filter_by=None, labels=None, column="Duration_miliseconds", colors=None
):
    if not colors:
        colors = [
            "red",
            "orange",
            "gold",
            "lime",
            "darkgreen",
            "lightsteelblue",
            "darkblue",
            "rebeccapurple",
            "violet",
            "black",
            "hotpink",
            "brown",
        ]
    if filter_by:
        datasets = apply_filter(datasets, filter_by)
    if not labels:
        labels = [str(num + 1) for num in range(len(datasets))]
    # Now, loop through all datasets.
    timestamp_groups = []
    datapoint_groups = []
    group_labels = []
    if group_by:
        for idx, df in enumerate(datasets):
            groups = {}
            for group, time, datapoint in zip(df[group_by], df["TimeFromStart_seconds"], df[column]):
                if group not in groups:
                    groups[group] = [[], [], str(labels[idx]) + ": " + str(group)]

                groups[group][0].append(time)
                groups[group][1].append(datapoint)

            for key in groups.keys():
                timestamp_groups.append(groups[key][0])
                datapoint_groups.append(groups[key][1])
                group_labels.append(groups[key][2])
    else:
        for idx, df in enumerate(datasets):
            timestamp_groups.append(df["TimeFromStart_seconds"])
            datapoint_groups.append(df[column])
            group_labels.append(labels[idx])

    return timestamp_groups, datapoint_groups, group_labels, colors


def apply_filter(datasets, filter_by=None):
    dfs = []
    if filter_by:
        # create a copy, to be modified
        for df in datasets:
            dfs.append(df.copy())

        for idx in range(len(dfs)):
            for col, value in filter_by:
                if value:
                    dfs[idx] = dfs[idx][dfs[idx][col] == value]
                else:
                    dfs[idx] = dfs[idx][dfs[idx][col] != None]

    else:
        dfs = datasets
    return dfs
