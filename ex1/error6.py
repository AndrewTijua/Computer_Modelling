"""
Create a list of random integers, then delete the even entries,
then print the remaining entries.
"""

import random

# Create and print a list of 20 integers
# where all entries are 0<=n<=100
numbers = [random.randint(0,100) for n in range(20)]
print("Original list:")
print(numbers)

numbers = [x for x in numbers if x%2==1] #Sets numbers to contain only odd entries
        

# Print the remaining list with all odd numbers
print("Odd entries:")
print(numbers)
