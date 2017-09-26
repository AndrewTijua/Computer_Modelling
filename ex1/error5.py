"""
Get an integer number from the user, then print out 
multiples of 3, 5, and 15, for all integers
up to and including that number.
"""

import sys

# Short introduction of code purpose
print("Fizzbuzz game: print all integers up to")
print("a user-given maximum, and exclaim")
print("Fizz/Buzz/Fizzbuzz for multiples of 3/5/15.")
print("-------------------------------------------")


# Get maximum integer from command line
try:
    max_int = int(sys.argv[1])
except:
    print("Wrong number of arguments.")
    print("Usage: python3 " + sys.argv[0] + " <number>")
    print("Code will print out multiples of 3, 5, and both,")
    print("in the integer range 1 to <number>.")
    sys.exit(-1)

if max_int<0:
    print("Error: integer must be greater than zero.")
    sys.exit(-2)

for i in range(max_int):
    if (i%3==0 and i%5==0):
        print(i, "Fizzbuzz")
    else:
        if i%3==0:
            print(i, "Fizz")
        if i%5==0:
            print(i, "Buzz")
        else:
            print(i)
