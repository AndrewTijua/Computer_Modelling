"""
This program takes a filename from the command-line and produces both a plot and data points for the given harmonic series
"""
import sys
import math
from matplotlib import pyplot
from numpy import linspace

"""
This function computes the harmonic function

param x: function input
param n: highest n in series to compute (sin(x), 1/3 sin(x), ...)
return: value of harmonic at x
"""
def harmonic(x, n):
    if n % 2 == 0:
        n = n+1
    
        
    retvalue = 0
    for i in range(1,n+1,2): #computes harmonic using for loop
        retvalue = retvalue + ((1/i)*math.sin(i * x)) 

    return retvalue

"""
This function handles the file i/o
return: no values, outputs graph and file
"""
def main():
    try: #Closes nicely if no CLAs given
        filename = str(sys.argv[1])
    except: 
        print("Wrong number of arguments!")
        print("Usage: python3 {0} <filename> <n_max>".format(sys.argv[0]))
        print("Please include file extension")

    try:
        n_max = int(sys.argv[2])
    except:
        n_max = 7

    try: #Attempts to open file (possible permission error
        file = open(filename, 'w')
    except:
        print("Please give a valid file")


    number_points = 1000 #initialises variables
    period = 2*math.pi

    x_space = linspace(0, period, number_points) #creates a list of number_points evenly spaced points
    x_vals = [] #initialises empty lists for plotting values
    y_vals = []
    x_new = 0
    y_new = 0


    for i in range(number_points): #tabulate function
        x_new = x_space[i]
        y_new = harmonic(x_new, n_max)
        x_vals.append(x_new)
        y_vals.append(y_new)
        file.write(str(x_new) + " " + str(y_new) + "\n")

    pyplot.plot(x_vals, y_vals)
    pyplot.suptitle("Plotting a harmonic function")
    pyplot.xlabel("X")
    pyplot.ylabel("H(X)")
    file.close()
    pyplot.show()


if __name__ == "__main__": main()
    
