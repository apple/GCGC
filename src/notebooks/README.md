# How to use a Jupyter notebook

Note: Notebooks rely on a kernel running a version of Python3. Currently, all notebooks and scripts have been written and tested using `Python 3.9.5`.

> # What is a notebook?

- A notebook consists of `cells`. Each cell contains independent code that can be run. The output for a cell appears below the cell itself. To analyze data using a notebook, a user would select cells to run, and view their outputs. 


- Variables defined anywhere within a cell are accessible throughout all cells above and below. (Does not apply to variables in a function's scope)Therefore, it is typical to create a variable in one cell, and reference it in the future.

A typical cell relationship may work as follows:

--- 
In \[1]: 

    print("Hello")

    var = "jupyter-notebooks"
Hello

---

In \[2]:

    print(var)

jupyter-notebooks

--- 

Where the number `x` after  `In[x]` means the cell's most recent run number (based on all cells ever run)



> # How to use notebooks for log analysis
In this particular project, all cells are associated with a certain type of `graph`, `chart`, or `comparison`. The typical workflow is as follows:



1. Set the file name / file path to the log to analyze. 
2. Select the top cell with the cursor
3. Run all cells, starting with the top cell
    - On web based Jupyter, select `Cell`-> `Run all`
4. View output.
