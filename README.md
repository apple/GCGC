# GCGC
## Garbage Collection Graph Collector 

<img src="images/pauses_scatterplot.jpg" alt="Example heat map plot" height="auto" />

This GC log analysis tool using a Juputer notebooks interface is useful for parsing gc log files created from java workloads. 
Currently supports collectors in both JDK11 & JDK 16.


 # Requirements to run

- Python3 
- The following Python3 packages
    - numpy
    - pandas
    - matplotlib
    - Jupyter notebook 

Setup for these explained in [setup.md](./setup.md)



# How to run analysis

Follow the instructions in [how-to-run.md](how-to-run.md)

# File Structure

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