# Simplex Method, Transportation Problem, and Hungarian Method

## Simplex Method

The Simplex method is a mathematical technique applicable to problems with any number of variables and constraints. It involves forming the augmented form of the linear problem (reconstruction of constraints), resulting in a set of 𝑛 + 𝑚 variables. Of these, 𝑛 variables are set to 0, while the remaining 𝑚 variables receive concrete values from 𝑚 equations.

### Initialization Steps

1. Identify the variable that will most significantly improve the optimality criterion.
2. Determine the maximum allowable increase for the selected variable without violating constraints.
3. Update variable values (basic and non-basic).
4. Repeat the process until the optimality criterion cannot be further improved.

### Optimal Solution

Once the optimality criterion cannot be improved, the solution is considered optimal.

## Transportation Problem

The Transportation problem involves 𝑛 initial points, each with its capacity, and 𝑚 final points, each with its demand. The goal is to distribute resources from initial to final points, representing variables (𝑚 * 𝑛), while minimizing the associated costs. This problem is characterized as an integer programming problem.

### Problem Formulation

Minimize 𝑧 = ∑ ∑ 𝑐𝑖𝑗𝑥𝑖𝑗, where 𝑖 = 1,2, … ,𝑛 and 𝑗 = 1,2, … ,𝑚.

Subject to:
a) ∑ 𝑥𝑖𝑗, 𝑗=1 to 𝑚 = 𝑆𝑖, 𝑖 = 1,2, … ,𝑛
b) ∑ 𝑥𝑖𝑗, 𝑖=1 to 𝑛 = 𝐷𝑗, 𝑗 = 1,2, … ,𝑚

### Initial Solution Methods

- Northwest corner method: Filling cells column-wise starting from the northwest corner.
- Minimum cost method: Filling cells with the lowest costs in ascending order.
- Vogel's method: Determining the difference between the two smallest costs in each row and column and filling the cell with the lowest cost.

### Solution Algorithm

The algorithm is based on potentials, with additional rows and columns representing potentials. It involves iteratively updating potentials and determining the optimal solution.

## Hungarian Method

The Hungarian method is applied to assignment problems, where resources need to be assigned to tasks with minimal costs or maximal profits.

### Key Steps

1. Transform the cost matrix by subtracting the minimum element in each row and column.
2. Mark independent zeros, starting from rows with only one zero.
3. Cross out rows and columns containing marked zeros.
4. Repeat until reaching an optimal solution, adjusting values based on the smallest uncrossed element.

The algorithm involves a systematic process of marking and crossing out until the optimal solution is achieved.

## Job Assignment Method

The Job Assignment method deals with variables 𝑥𝑖𝑗, indicating whether a worker 𝑖 performs a job on machine 𝑗. Costs 𝑐𝑖𝑗 represent the time required for worker 𝑖 to complete the job on machine 𝑗.

### Constraints

  a) ∑ 𝑥𝑖𝑗, 𝑗=1 to 𝑛 = 1, 𝑖 = 1,2, … ,𝑛

  b) ∑ 𝑥𝑖𝑗, 𝑖=1 to 𝑛 = 1, 𝑗 = 1,2, … ,𝑛

### Solution Procedure

  a) Transform the cost matrix by subtracting the minimum element in each row and column.

  b) Mark independent zeros, starting from rows with only one zero. If the number of independent zeros matches the number of workers, an optimal solution is found.

  c) Cross out rows and columns containing marked zeros until no further steps are possible.

  d) Subtract the smallest uncrossed element from all uncrossed elements and add it to the intersection of lines.

  e) Repeat the process until an optimal solution is reached.

This algorithm ensures an efficient assignment of jobs to workers while minimizing the overall completion time.
