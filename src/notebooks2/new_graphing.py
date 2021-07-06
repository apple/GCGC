import matplotlib.pyplot as plt
from numpy import rot90
from apply_restrictions import apply_restrictions


def scatter2(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    column="Duration_miliseconds",
    labels=None,
    axs=None,
    colors=None,
):
    # Verify parameters are correct
    if not gc_event_dataframes:
        print("No gc_event_dataframes passed into scatter")
    assert isinstance(gc_event_dataframes, list)
    if not labels:
        labels = [str(idx) for idx in range(len(gc_event_dataframes))]
    if not axs:
        fig, axs = plt.subplots()
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
    # Apply filters, in an "AND" style: Filters must meet ALL conditions
    dfs = []
    if filter_by:
        # create a copy, to be modified
        for df in gc_event_dataframes:
            dfs.append(df.copy())

        for idx in range(len(dfs)):
            for col, value in filter_by:
                if value:
                    dfs[idx] = dfs[idx][dfs[idx][col] == value]
                else:
                    dfs[idx] = dfs[idx][dfs[idx][col] != None]

    else:
        dfs = gc_event_dataframes

    # plot the data
    if group_by:  # TODO: this is slow.
        group_count = 0
        for idx, df in enumerate(dfs):
            found_groups = {}
            for group, time, datapoint in zip(df[group_by], df["TimeFromStart_seconds"], df[column]):
                if group:
                    if group in found_groups:
                        plt.scatter(time, datapoint, color=found_groups[group])
                    else:
                        found_groups[group] = colors[group_count]
                        plt.scatter(time, datapoint, color=found_groups[group], label=(labels[idx] + " " + str(group)))
                        group_count += 1

    else:
        for idx, df in enumerate(dfs):
            plt.scatter(df["TimeFromStart_seconds"], df[column], color=colors[idx], label=labels[idx])
    # Missing: User must set y label.
    axs.legend()
    axs.set_xlabel("Time passed in seconds")
    return axs


def scatter(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    axs=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, colors = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    if not axs:
        f, axs = plt.subplots()

    for time, datapoints, color, label in zip(timestamp_groups, datapoint_groups, colors, labels):
        axs.scatter(time, datapoints, label=label, color=color)
    axs.legend()
    return axs


def line(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    axs=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, colors = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    if not axs:
        f, axs = plt.subplots()

    for time, datapoints, color, label in zip(timestamp_groups, datapoint_groups, colors, labels):
        axs.plot(time, datapoints, label=label, color=color)
    axs.legend()
    return axs


def pie_sum(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    ax=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, colors = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    if not ax:
        f, axs = plt.subplots()

    pie_slices_sizes = []
    for thing in datapoint_groups:
        print(thing)
    for idx, datapoints in enumerate(datapoint_groups):
        pslice = sum(datapoints)
        pie_slices_sizes.append(slice)
        labels[idx] = labels[idx] + " : " + str(pslice)
    axs.pie(pie_slices_sizes, labels=labels, colors=colors, startangle=-40)
    axs.legend()
    return axs


def bar_sum(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    axs=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, colors = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    if not axs:
        fig, axss = plt.subplots()

    for idx, (datapoints, color, label) in enumerate(zip(datapoint_groups, colors, labels)):
        barheight = sum(datapoints)
        axss.bar(idx, barheight, label=label + " : " + str(round(barheight, 4)), color=color)
    axss.set_xticks(range(len(datapoint_groups)))
    axss.set_xticklabels(labels)
    axss.legend()
    return axss


def bar_avg(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    axs=None,
    column="Duration_miliseconds",
):

    _, datapoint_groups, labels, colors = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    if not axs:
        f, axss = plt.subplots()

    for idx, (datapoints, color, label) in enumerate(zip(datapoint_groups, colors, labels)):
        barheight = sum(datapoints) / len(datapoints)
        axss.bar(idx, barheight, label=label + " : " + str(round(barheight, 4)), color=color)
    axss.set_xticks(range(len(datapoint_groups)))
    axss.set_xticklabels(labels)
    axss.legend()
    return axss


from src.graphing.trends import compare_trends


def trends(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    axs=None,
    column="Duration_miliseconds",
    throughput=False,
):
    timestamp_groups, datapoint_groups, labels, _ = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column
    )
    if throughput:
        compare_trends(datapoint_groups, labels=labels, lists_of_timestamps=timestamp_groups)
    else:
        compare_trends(datapoint_groups, labels=labels)


from src.graphing.percentiles import compare_pauses_percentiles


def percentiles(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    axs=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, _ = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column
    )
    compare_pauses_percentiles(datapoint_groups, labels=labels)


def reclaimed_bytes(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    axs=None,
    column="Duration_miliseconds",
):
    if not axs:
        fig, axs = plt.subplots()

    # Access the beforeGC data

    timestamp_groups, datapoint_groups_before, _, colors = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, "HeapBeforeGC"
    )

    # Access the beforeGC data
    timestamp_groups, datapoint_groups_after, _, _ = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, "HeapAfterGC"
    )
    reclaimed_bytes_groups = []
    for before_gc, after_gc in zip(datapoint_groups_before, datapoint_groups_after):
        reclaimed_bytes_groups.append([before - after for before, after in zip(before_gc, after_gc)])

    for time, datapoints, color, label in zip(timestamp_groups, reclaimed_bytes_groups, colors, labels):
        axs.scatter(time, datapoints, label=label, color=color)
    axs.legend()
    return axs
