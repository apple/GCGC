# Setup

>This section explains how to locally install python3, jupyter notebook, and any needed python packages (such as matplotlib). Explanation assumes you are running macOS locally on BigSur
## Part 1 - Python 3
The official documentation can be found here:  [Python setup MacOS](https://docs.python.org/3/using/mac.html)

However, you are welcome to follow this guide.
> Important notice (from official documentation): 

> The Apple-provided build of Python is installed in `/System/Library/Frameworks/Python.framework` and `/usr/bin/python`, respectively. You should never modify or delete these, as they are Apple-controlled and are used by Apple- or third-party software. Remember that if you choose to install a newer Python version from python.org, you will have two different but functional Python installations on your computer, so it will be important that your paths and usages are consistent with what you want to do.

1. Open the [Python download page](https://www.python.org/downloads/mac-osx/), and download the latest Python 3 Release
2. Navigate to the latest version, and download "macOS 64-bit universal2 installer" from the files section at the bottom of the download page.
3. Open the python-3.x.x-macos.pkg file you have installed. Follow the installation instructions in the installer application. (Feel free to move the installer to the garbage after installation)
4. Open a terminal , and verify you successfully installed python3, and the the correct version is on path by running `python3 --version`. Confirm the output matches something like `Python 3.9.5`
5. (If step 4 did not work) : Navigate the Python3.x folder in your `Applications` folder. Open the folder, and run the following program: `Update Shell Profile.command`
6. Repeat step 4. If lost, follow the official documentation for more setup guidance and troubleshooting

## Installing additional packages
You can use pip package manager to install additional packages.
1. Check if pip is already installed. Type `python3 -m pip --version`
2. Use `pip3` for installing packages. 
3. `pip3 install <package name>`. 
(For Example: `pip3 install matplotlib`)
4. If you do not already have pip3 installed , you may need to update the version. Follow the command line error output to update the version, if needed. Otherwise, follow [this guide](https://packaging.python.org/tutorials/installing-packages/) in the offical python documentation 
5. Currently, the following packages are needed. Install all.
    - matplotlib 
    - pandas
    - numpy


## Part 2 - Jupyter notebooks
You can find the official documentation on how to install [here](https://jupyter.org/install)

1. Install using `pip3 install notebook`
2. Navigate to the [correct folder](https://github.pie.apple.com/ellis-brown/gc-analysis/tree/main/Jupyter-everything), that holds your `.ipynb` files. 
3. run `jupyter notebook` in terminal to launch a local notebook server
4. Use the web based notebook to interact with the notebook
> Note: You can use some IDEs to edit and run your Jupyter-notebook, if desired. One example is VS-Code, which lets you run the notebook locally, if the server is being hosted.