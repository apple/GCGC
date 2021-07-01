# Gc log analysis
#### Ellis Brown (7/1/2021)

#
Jupyter notebooks designed for easy and useful parsing of log files created from java workloads. Currently supports Shenandoah, G1, Parallel, Serial, and Z garbage collectors in JDK11.


> ## Requirements to run

- Python3 
- The following Python3 packages
    - numpy
    - matplotlib
    - re
    - Jupyter notebook 

Setup for these explained in [setup.md](./setup.md)

## How to run analysis

1. Navigate to `src/`
2. Run the terminal command `jupyter notebook` under `src/` or open a notebook using a compatible IDE. This will begin a python3 kernel to execute commands.
3. Open ``notebook_compare_logs.ipynb`` or ``notebook_single_log.ipynb``
4. Set the path to your log file in the second cell
4. Use the in-notebook instructions to run analysis, or run all cells.


## File Structure

> datasets
> > - ` long/` - contains example log files
> > - `short/`- contains example log files

> src
> > - `graphing/` - contains plotting and graphing python scripts
> > - `notebooks/` - contains notebooks to analyze log files with.
> > - `*.py` - contains python scripts for Jupyter notebooks

> tests
> > - testing infrastructure and datasets
