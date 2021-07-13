# GC log analysis
#### Ellis Brown (7/13/2021)

#
This GC log analysis tool using a Juputer notebooks interface is useful for parsing gc log files created from java workloads. 
Currently supports Shenandoah, G1, Parallel GC, Serial GC, and Z garbage collectors in JDK11.


> ## Requirements to run

- Python3 
- The following Python3 packages
    - numpy
    - matplotlib
    - Jupyter notebook 

Setup for these explained in [setup.md](./setup.md)

## How to run analysis

1. Navigate to `src/notebooks`
2. Run the terminal command `jupyter notebook` under `src/notebooks` or open a notebook using a compatible IDE. This will begin a python3 kernel to execute commands.
3. Open ``compare_any.ipynb`` in the web page that opened as a result of running the above command. If using an IDE, open the file from `src/notebooks`
4. Set the second code cell's state information
   - `files` : a list of log files to be analyzed
   - `labels`: describe the log files listed above. 
   - `time_range_seconds` : Minimum and maximum time, or None for the whole file
4. Use the in-notebook instructions to run analysis, or run all cells at the top. For help running cells, view the notebooks in `/tutorials`.


## File Structure

> datasets
> > - ` long/` - contains example log files. 
> > - `short/`- contains example log files

> src
> > - `graphing/` - contains plotting and graphing python scripts
> > - `notebooks/` - contains notebooks to analyze log files with.
> > - `*.py` - contains python scripts to aid in simplicity of the Jupyter notebook interface

> [setup.md](setup.md) - contains instructions on how to setup the required parts of this project