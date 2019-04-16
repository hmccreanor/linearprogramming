from math import inf
import numpy as np

# Supress divide by 0 warnings
np.seterr(divide="ignore")

tableu = np.array([[1, 1, 1, 1, 0, 0, 0, 600],
                   [1, 3, 0, 0, 1, 0, 0, 600],
                   [2, 0, 1, 0, 0, 1, 0, 900],
                   [-60, -90, -300, 0, 0, 0, 1, 0]])

slack_start_index = 3

constraint_index = tableu.shape[1] - 1
bottom_index = tableu.shape[0] - 1

variable_values = tableu[bottom_index][:slack_start_index]

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


print(tableu)


