import process_log as pl
import plot_data as dplt

def main():
    
    # testInitialHeapState()
    # testHeapAllocation()
    testLargeInformationPauseCollection()
    
    #dplt.plot_heap_allocation_breakdown(temp)
    #df = pl.getPauses(False)
    #dplt.plot_pauses(df)
    
def testLargeInformationPauseCollection():
    pl.setLogPath("../../datasets/amzn_workload_4.log")
    t = pl.getGCdataSections()



def testHeapAllocation():
    pl.setLogPath("../../datasets/amzn_workload_4.log")
    pl.setLogSchema(0)
    print("First run:\n")
    t = pl.getHeapAllocation(False)
    dplt.plot_heap_allocation_breakdown(t)

    pl.setLogPath("../../datasets/gc.log")
    pl.setLogSchema(1)
    print("Second Run:\n")
    t = pl.getHeapAllocation(False)
    dplt.plot_heap_allocation_breakdown(t)


def testInitalHeapState():
    pl.setLogPath("../../datasets/amzn_workload_4.log")
    pl.setLogSchema(0)
    print("First run: " , pl.getHeapInitialState(False))


    pl.setLogPath("../../datasets/gc.log")
    pl.setLogSchema(1)
    print("Second Run: ", pl.getHeapInitialState(False))
    


main()