### Purpose: Extracts the time information for any GC log line.
### Returns both time stamps, in their entirety.


def get_timestamps(line):
    ## We assume we are extracting a line, following the following
    ## format.
    #[2020-11-16T14:54:23.755+0000][7.353s][info ] ...
    if not line[0] == "[":
        return None
    # Now, we assume we have a valid line. Extract information based on this assumption.    
    index_seperator = line.index("]")
    real_time  = line[1:index_seperator]
    from_start = line[index_seperator + 2 : index_seperator + 2 + line[index_seperator + 2:].index("]")]
    return [real_time, from_start] 
