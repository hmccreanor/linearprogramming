# This module will parse linear expressions in standard form and generate a tableu from them

# Linear expressions should come from a file of the following (annotated) form:

# 3x + 10y - 5z  <- objective function to be MAXIMISED (should contain all variables (not slack ones))
# 3 <- number of linear expressions 
# 5x + 3y LT 50
# 6z - 2x LT 10
# x + z LT 6

import re
import numpy as np

# Returns an array of the form [tableu, slack_start_index]
def parse(inFile):
    with open(inFile, "r") as f:
        lines = f.readlines()

        objective_function = lines[0].rstrip()
        n_expressions = int(lines[1].rstrip())
        expressions = lines[2:]

        objective_coefficients = {}

        # Parse objective function

        objective_symbols = objective_function.split(" ")

        next_symbol_sign = 1
        for objective_symbol in objective_symbols:
            if objective_symbol == "+":
                next_symbol_sign = 1
            elif objective_symbol == "-":
                next_symbol_sign = -1
            else:
                objective_symbol = [x for x in re.split("(\d+)", objective_symbol) if x != ""] # List comprehension used because split has a "" element in the list it returns
                objective_coefficients[objective_symbol[1]] = next_symbol_sign * int(objective_symbol[0])
         
        variables = list(objective_coefficients.keys())
        # Parse expressions

        coefficient_table = [{} for i in range(len(expressions))] # Stores coefficients and variables for each linear expression
        constraints = [] # Stores RHS of each linear expression

        for i in range(n_expressions):
            expression = expressions[i]
            expression_symbols = expression.rstrip().split(" ")
            next_symbol_sign = 1
            for j in range(len(expression_symbols) - 1):
                expression_symbol = expression_symbols[j]
                if expression_symbol == "+":
                    next_symbol_sign = 1
                elif expression_symbol == "-":
                    next_symbol_sign = -1
                elif expression_symbol == "LT":
                    #constraints[i] = int(expression_symbols[j + 1])
                    constraints.append(int(expression_symbols[j + 1]))
                else:
                    expression_symbol = [x for x in re.split("(\d+)", expression_symbol) if x != ""] # List comprehension used because split has a "" element in the list it returns
                    if len(expression_symbol) == 1:
                        coefficient_table[i][expression_symbol[0]] = next_symbol_sign
                    else:
                        coefficient_table[i][expression_symbol[1]] = next_symbol_sign * int(expression_symbol[0])
            
            # Set coefficients of variables not in expression to 0
            variables_in_expression = list(coefficient_table[i].keys())
            for variable in variables:
                if variable not in variables_in_expression:
                    coefficient_table[i][variable] = 0


        # Construct tableu
        n_slack = n_expressions
        n_variables = len(objective_coefficients.keys())

        tableu = np.zeros((n_expressions + 1, n_variables + n_slack + 2), dtype=np.intc)

        # Update the rows regarding the linear expressions
        for i in range(n_expressions):
            count = 0 # Storing the row index 
            for variable in variables:
                tableu[i][count] = coefficient_table[i][variable]
                count += 1
            tableu[i][count + i] = 1 # Set the respective slack variable coefficient to be 1
            tableu[i][n_variables + n_slack + 1] = constraints[i] # Set the last element in the row to be the constraint for that particular linear expression

        # Update the last row
        for i in range(n_variables):
            variable = variables[i]
            tableu[n_expressions][i] = -1 * objective_coefficients[variable]

        tableu[n_expressions][n_variables + n_slack] = 1 # Set "score" variable coefficient to 1

        return [tableu, n_variables]

