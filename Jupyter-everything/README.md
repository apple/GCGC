## /Jupyter-everything/

- `/Jupyter-everything/datasets/`
    - symbolic link to local files. To access
the files, download through box using this link [datasets](https://apple.box.com/s/vcqgyxx8x1jesyj8smc9ow31kpd5u73b)
- `/Jupyter-everything/scripts`
    - Scripts used for log parsing and data plotting.
    
- `compare_multiple.ipynb`
    - Allows for log comparison of multiple logs
    - Note: Less comparison currently implemented than in log_analysis
- `log_analysis.ipynb`
    - Full analysis of one log

- `jfr_zulu_stats.ipynb`
    - Compares output this my gc log parsing with Java Flight Recorder. 
    - Note: Required to manually create CSV from flight recorder file.
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
