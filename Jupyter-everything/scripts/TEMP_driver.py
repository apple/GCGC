import process_log

def main():
    process_log.setLogPath("../../datasets/gc.log")
    process_log.getPauses( False)

main()
