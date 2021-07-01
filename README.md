# Gc log analysis
#### Ellis Brown (7/1/2021)


### Parse log files created from Java gc

> ## How to run analysis
(requirements)
- python3 and used packages (numpy, matplotlib, matplotlib.pyplot, re)
- Jupyter notebook
Setup for both explained in [Jupyter-everything/setup](https://github.pie.apple.com/ellis-brown/gc-analysis/tree/main/Jupyter-everything/setup)

(begin analysis)           
1. Navigate to /Jupyter-everything/
2. type  `jupyter notebook`
3. open ``log analysis`` or ``compare_multiple``
4. Use the in-notebook instructions to run analysis

> ### File Structure

- /Jupyter-everything
    - All Jupyter notebook related files. Contains all needed code for this project

- /datasets
   
    - Note: When using a notebook, the 'datasets' file referenced is /Jupyter-everything/datasets. This is not the same folder, but where my actual datasets live: this folder is included in the gitignore. It is recommended that you use this folder for local files

>
    To Nitsan: 

    If you are code reviewing, the following files are interesting.


    /Jupyter-everything/scripts/parse_log.py
    /Jupyter-everything/scripts/compare_log.py
    /Jupyter-everything/scripts/g1version16.py
    /Jupyter-everything/scripts/plot_data.py

    /Jupyter-everything/compare_multiple.ipynb
    /Jupyter-everything/log_analysis.ipynb

    If you are running low on time, I think I could use the most help with `parse_log.py and any of the notebooks, I have never worked with a notebook before and don't know whats expected for presentation `
