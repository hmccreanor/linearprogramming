# Simplex Algorithm

Implementation of the simplex algorithm. Reads linear expressions in from a text file, converts them to a tableu which can be used to run the simplex algorithm. Runs the simplex algorithm on the tableu. Returns the tableu. Boom sorted.


The format of the linear expression specification file is as follows:

```
Function to optimize
Number of constraints
Constraint 1
Constraint 2
Constraint 3
...
Constraint n
```

An example input file is specified below:
```
60x + 90y + 300z
3
x + y + z LT 600
x + 3y LT 600
2x + z LT 900
```
**N.B** LT stands for 'less than or equal to'

## Todo:
+ Implement pretty printing of optimal results
