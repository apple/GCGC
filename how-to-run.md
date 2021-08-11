# How to run analysis

### 1. Open up a terminal window, and navigate to `src/notebooks` in this GCGC tool.

<img src="images/terminal_start.jpg" alt="terminal window in correct directory" />

--- 

### 2. Run the terminal command `jupyter notebook` under [src/notebooks](./src/notebooks) or open a notebook using a compatible IDE such as VSCode. This will begin a python3 kernel to execute commands.

<img src="images/open_notebook_with_terminal.jpg" alt="Opening notebook using terminal" />

---

### 3. Open [GCGC.ipynb](./src/notebooks/GCGC.ipynb) in the web page that opened as a result of running the above command. If using an IDE, open the file from [src/notebooks](src/notebooks)

<img src="images/open_tree_notebooks.jpg" alt="Opening jupyter notebooks tree" />

---

### 4. Set the second code cell's required state information. There will be an example already filled out.
   - `files` : a list of log files to be analyzed
   - `labels`: describe the log files listed above. 

<img src="images/set_filepaths_and_labels.jpg" alt="Setting the state variables"/>

---

### 5. Run all cells. In the web based Jupyter notebooks, press `Cell` from the top menu, and select `Run All`. If you are working from an IDE rather than web based Jupyter, follow the online documentation for your particular IDE.  

<img src="images/run_all_cells.jpg" />

--- 

### 6. After that, the analysis should be automatically generated!