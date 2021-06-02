from matplotlib import pyplot as plt
import random as r 

def main():
    fig, ax = plt.subplots()
    
    ax = addLabels(ax)
    colors = ["g", "r", "b", "y"]
    for i in range(4):
        ax = someFunction(ax, colors[i])
    plt.show()

def someFunction(ax, c):
    ax.plot([20 * r.randint(2, 20) for x in range(r.randint(4,8))], color = c)
    
    
    
    return ax 

def addLabels(ax):
    ax.set_xlabel("X LABEL")
    ax.set_ylabel("Y LABEL")
    return ax 

main()