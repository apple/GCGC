import pandas as pd
import matplotlib.pyplot as plt

path='/Users/ellisbrown/Desktop/Project/bucket_parse/ex.csv'


column_titles = ["Time, Memory Changed"]
df = pd.read_csv(path)
    #print(list(df.iloc[:,0]))
    #csv_reader=csv.reader(csv_file, delimiter=",", usecols = column_titles)
x_values = list(df.iloc[:,3])
x = []
for entry in x_values:
    x.append(entry[:-1])
y_values = list(df.iloc[:,0])
## Only plot the first 5, due to label confusion. TODO.
max_items = 10 #len(y_values) for max
plt.bar(x = x[:max_items], height = y_values[:max_items])


plt.ylabel("Miliseconds wait");

## Find interesting trends within the data.
def find_trends(df):
    wait_times = list(df.iloc[:,0])
    max_wait = max(wait_times, key = lambda i : float(i))
    print("Max wait: " + str(max_wait) + " ms")
    
    total_wait   = round(sum(float(i) for i in wait_times), 4)
    average_wait = round(total_wait / len(wait_times), 4)
    print("Total wait: " + str(total_wait) + " ms")
    print("Average wait: " + str(average_wait) + " ms")
find_trends(df)

############################################################
from scripts.ex import some_function
some_function()


    