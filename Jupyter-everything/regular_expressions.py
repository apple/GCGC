
### Example one: Getting the groups out of any line. 
        # group 1 : (DATE-TIME)
        # group 2 : (TIME FROM START)
        # group 3 : (info/debug/...) 
        # group 4 : (gc, phases, ...)
        # group 5: (everything else on that line)
#[0.549s][debug][gc,phases    ] GC(0)     Code Roots Fixup: 0.0ms
#[2020-11-16T14:54:16.417+0000][0.015s][trace][gc,task      ] WorkerManager::add_workers() : created_workers: 1
line_parse = '/\[*(.*)\]*\[\d+\.\d+\w+\]\[(.*)\[(.*)\](.*)/gm'
        #     ^                                           ^^^
        #     things with arrows probably not needed for re expression   
