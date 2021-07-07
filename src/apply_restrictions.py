import math


def apply_restrictions(
    datasets, group_by=None, filter_by=None, labels=None, column="Duration_miliseconds", colors=None
):
    if not colors:
        colors = []
        for index in range(1, len(datasets) + 1):
            color = (
                abs(math.cos(index * math.pi * 2 / 3)),
                abs(math.cos(index * 25 * 4 / 3)),
                abs(math.cos(index * 11)),
            )
            colors.append(color)
    if filter_by:
        datasets = apply_filter(datasets, filter_by)
    if not labels:
        labels = [str(num + 1) for num in range(len(datasets))]
    # Now, loop through all datasets.
    timestamp_groups = []
    datapoint_groups = []
    group_labels = []
    log_number_list = []
    if group_by:
        for idx, df in enumerate(datasets):
            groups = {}
            for group, time, datapoint in zip(df[group_by], df["TimeFromStart_seconds"], df[column]):
                if group:
                    if group not in groups:
                        groups[group] = [[], [], str(labels[idx]) + ": " + str(group)]
                    groups[group][0].append(time)
                    groups[group][1].append(datapoint)

            for key in groups.keys():
                timestamp_groups.append(groups[key][0])
                datapoint_groups.append(groups[key][1])
                group_labels.append(groups[key][2])
                log_number_list.append(idx)

    else:
        for idx, df in enumerate(datasets):
            timestamp_groups.append(df["TimeFromStart_seconds"])
            datapoint_groups.append(df[column])
            group_labels.append(labels[idx])
            log_number_list.append(idx)

    return timestamp_groups, datapoint_groups, group_labels, colors, log_number_list


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
                    import pandas as pd

                    dfs[idx] = dfs[idx][pd.notnull(dfs[idx][col])]
    else:
        dfs = datasets
    return dfs
