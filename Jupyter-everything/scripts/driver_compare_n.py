# import sys
# sys.path
# sys.path.append('/Users/ellisbrown/Desktop/Project/Jupyter-everything/scripts/__init__.py')

from scripts import compare_logs as cl

def main():
    files = []
    files.append("/Users/ellisbrown/Desktop/Project/datasets/long_a.log")
    files.append("/Users/ellisbrown/Desktop/Project/datasets/small_simlog.log")
    files.append("/Users/ellisbrown/Desktop/Project/datasets/amzn_workload_4.log")
    files.append("/Users/ellisbrown/Desktop/Project/datasets/long_amzn_workload.log")
    cl.setFiles(files)
    cl.compareMetadata()
    #cl.comparePauses()
    print("finished!")


main()