import process_log

def main():
    process_log.setLogPath("../../datasets/gc.log")
    df = process_log.getPauses(False)
    print(df)

main()
