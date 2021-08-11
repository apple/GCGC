# GCGC
## Garbage Collection Graph Collector 

<img src="images/s2.jpg" alt="Example heat map plot" height="300px" />

This GC log analysis tool using a Juputer notebooks interface is useful for parsing gc log files created from java workloads. 
Currently supports collectors in both JDK11 & JDK 16.


> ## Requirements to run

- Python3 
- The following Python3 packages
    - numpy
    - pandas
    - matplotlib
    - Jupyter notebook 

Setup for these explained in [setup.md](./setup.md)

## How to run analysis

1. Navigate to [src/notebooks](./src/notebooks)
2. Run the terminal command `jupyter notebook` under [src/notebooks](./src/notebooks) or open a notebook using a compatible IDE such as VSCode. This will begin a python3 kernel to execute commands.
3. Open [GCGC.ipynb](./src/notebooks/GCGC.ipynb) in the web page that opened as a result of running the above command. If using an IDE, open the file from [src/notebooks](src/notebooks)
4. Set the second code cell's required state information
   - `files` : a list of log files to be analyzed
   - `labels`: describe the log files listed above.    
5. Run all cells. In the web based Jupyter notebooks, press `Cell` from the top menu, and select `Run All`. If you are working from an IDE rather than web based Jupyter, follow the online documentation for your particular IDE.  


## File Structure

> [datasets](./datasets)
> > - [short/](./datasets/short) - contains example log files

> [src](./src)
> > - [graphing/](./src/graphing) - contains plotting and graphing python scripts
> > - [notebooks/](./src/notebooks) - contains notebooks to analyze log files with.
> > - [*.py](./src) - contains python scripts to aid in simplicity of the Jupyter notebook interface

> [setup.md](setup.md) - contains instructions on how to setup the required parts of this project

--- 

Note: Not all files are documented up to date fully:
The following files are still being documented.

- src/parse_log_file.py -> Correct, but improved documentation will be coming soon, to improve experience.
- src/graping/logarithamic_heatmap_testing.py
- src/graphing/allocation_rate.py