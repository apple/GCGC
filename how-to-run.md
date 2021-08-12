# How to run analysis

 It is expected that you are familiar with Jupyter notebooks. If not, please read this brief explanation from the official documentation: [Explanation](https://notebooks.gesis.org/binder/jupyter/user/ipython-ipython-in-depth-nvzdsac6/notebooks/examples/Notebook/Notebook%20Basics.ipynb)

### 1. Open up a terminal window, and navigate to `src/notebooks` in this GCGC tool.

<img src="images/terminal_start.jpg" alt="terminal window in correct directory" />

--- 

### 2. Run the terminal command `jupyter notebook` under [src/notebooks](./src/notebooks). This will begin a python3 kernel to execute commands. It will also open a web page in your default browser. The terminal output contains information on how to open the correct web page if it d

<img src="images/open_notebook_with_terminal.jpg" alt="Opening notebook using terminal" />

---

### 3. Open [GCGC.ipynb](./src/notebooks/GCGC.ipynb) in the web page that opened as a result of running the above command. 

<img src="images/open_tree_notebooks.jpg" alt="Opening jupyter notebooks tree" />

---

### 4. Set the first code cell's required state information. There will be an example already filled out.
   - `filepaths` : a list of log files to be analyzed
   - `labels`: describe the log files listed above. 

<img src="images/set_filepaths_and_labels.jpg" alt="Setting the state variables"/>

---

### 5. Run all cells. In the web based Jupyter notebooks, press `Cell` from the top menu, and select `Run All`.  

<img src="images/run_all_cells.jpg" />

--- 

### 6. After that, the analysis should be automatically generated! The plots will generate one by one starting from the top of the file. Each plot takes a few seconds to generate. After running all cells, scroll down to verify they have begun to run.
<img src="images/plot1_cells.jpg" alt="After running notebook cells" />
Notice, your cell's output has automatically been plotted inline. Wait for the full notebook analysis to finish, then analyze your results. Warning: An Error caused by a plot will prevent the following cells from executing. 

---

### 7. Wait for all cells to finish running.

<img src="images/running_cell.jpg" alt="Cell currently running" />

A cell that is running will have the term `In [ * ] :`

A cell that is finished running will have `In [ n ] :`, meaning that the cell was the n-th cell to be run.

---