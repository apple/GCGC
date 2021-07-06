import matplotlib.pyplot as plt
from apply_restrictions import apply_restrictions


def scatter2(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    column="Duration_miliseconds",
    labels=None,
    ax=None,
    colors=None,
):
    # Verify parameters are correct
    if not gc_event_dataframes:
        print("No gc_event_dataframes passed into scatter")
    assert isinstance(gc_event_dataframes, list)
    if not labels:
        labels = [str(idx) for idx in range(len(gc_event_dataframes))]
    if not ax:
        fig, ax = plt.subplots()
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
    ax.legend()
    ax.set_xlabel("Time passed in seconds")
    return ax


def scatter(
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
    ax=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, colors = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    if not ax:
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

    for idx, datapoints in enumerate(datapoint_groups):
        slice = sum(datapoints)
        pie_slices_sizes.append(slice)
        labels[idx] = labels[idx] + " : " + str(slice)
    axs.pie(pie_slices_sizes, labels=labels, colors=colors, startangle=-40)
    axs.legend()
    return axs


def bar_sum(
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
    for idx, (datapoints, color, label) in enumerate(zip(datapoint_groups, colors, labels)):
        barheight = sum(datapoints)
        axs.bar(idx, barheight, label=label + " : " + str(barheight), color=color)
    axs.set_xticks(range(len(datapoint_groups)))
    axs.set_xticklabels(labels)
    axs.legend()
    return axs


def bar_avg(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    ax=None,
    column="Duration_miliseconds",
):
    num_gc_logs = len(gc_event_dataframes)
    _, datapoint_groups, labels, colors = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    if not ax:
        f, axs = plt.subplots()
    for log in range(num_gc_logs):
        for idx, (datapoints, color, label) in enumerate(zip(datapoint_groups, colors, labels)):
            barheight = sum(datapoints) / len(datapoints)
            axs.bar(idx, barheight, label=label + " : " + str(barheight), color=color)
    axs.set_xticks(range(len(datapoint_groups)))
    axs.set_xticklabels(labels)
    axs.legend()
    return axs


from src.graphing.trends import compare_trends


def trends(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    ax=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, _ = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column
    )
    compare_trends(datapoint_groups, labels=labels, lists_of_timestamps=timestamp_groups)


from src.graphing.percentiles import compare_pauses_percentiles


def percentiles(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    ax=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, _ = apply_restrictions(
        gc_event_dataframes, group_by, filter_by, labels, column
    )
    compare_pauses_percentiles(datapoint_groups, labels=labels)
