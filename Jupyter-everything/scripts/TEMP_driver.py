import process_log as pl
import plot_data as pltd

def main():
    pl.setLogPath("../../datasets/gc.log")
    df = pl.getPauses(False)
    pltd.plot_pauses(df)
   

main()
