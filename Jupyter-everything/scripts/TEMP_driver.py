import process_log as pl
import plot_data as pltd

def main():
    pl.setLogPath("../../datasets/amzn_workload_4.log")
    #temp = pl.getHeapAllocation()
    pl.getHeapInitialState2()
    #pltd.plot_heap_allocation_breakdown(temp)
    #df = pl.getPauses(False)
    #pltd.plot_pauses(df)
   

main()
