import process_log as pl
import plot_data as pltd

def main():
    
    # testInitialHeapState()

    #pltd.plot_heap_allocation_breakdown(temp)
    #df = pl.getPauses(False)
    #pltd.plot_pauses(df)
    

main()


def testInitalHeapState():
    pl.setLogPath("../../datasets/amzn_workload_4.log")
    pl.setLogSchema(0)
    print("First run: " , pl.getHeapInitialState(True))


    pl.setLogPath("../../datasets/gc.log")
    pl.setLogSchema(1)
    print("Second Run: ", pl.getHeapInitialState(True))
    