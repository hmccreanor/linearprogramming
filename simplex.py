from math import inf
import numpy as np
from lExpParser2 import Tableu
import sys

inFile = sys.argv[1]

# Supress divide by 0 warnings
np.seterr(divide="ignore")

t = Tableu(inFile)
tableu = t.tableu
slack_start_index = t.slack_start_index
variables = t.variables

constraint_index = tableu.shape[1] - 1
bottom_index = tableu.shape[0] - 1

variable_values = tableu[bottom_index][:slack_start_index]

# Running the simplex algorithm
while np.any(variable_values < 0): # Some negative values in left part of tableu
    pivot_column = np.argmin(variable_values)

    row_min = inf
    pivot_row = 0
    divided = tableu[:,constraint_index] / tableu[:,pivot_column]

    for i in range(divided.size):
        n = divided[i]
        if n > 0 and n < row_min:
            row_min = n
            pivot_row = i

    # Pivoting
    for i in range(tableu.shape[0]):
        if i != pivot_row and tableu[i][pivot_column] != 0:
            tableu[i] = ((-1 * tableu[i][pivot_column]) * tableu[pivot_row]) + tableu[i]

print("Final tableu:")
print(tableu)
print(" ")

# Extracting the values of the variable coefficients
for i in range(slack_start_index):
    column = tableu[:,i]
    ones_count = 0
    one_index = 0
    exclusively_ones_and_zeros = True
    for j in range(len(column)):
        if column[j] == 1:
            ones_count += 1
            one_index = j
        elif column[j] != 0:
            exclusively_ones_and_zeros = False
            break

    if ones_count == 1 and exclusively_ones_and_zeros:
        print(variables[i], ":", tableu[one_index][tableu.shape[1] - 1])
    else:
        print(variables[i], ": 0")

