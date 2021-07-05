import matplotlib.pyplot as plt


def scatter(
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
                        print(colors)
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
