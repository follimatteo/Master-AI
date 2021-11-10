from minizinc import Instance, Model, Solver
import time


# NQueens basic resolution
nqueens = Model()
nqueens.add_string(
    '''
    int: n; % The number of queens.

    array [1..n] of var 1..n: q;

    include "alldifferent.mzn";

    constraint alldifferent(q);
    constraint
        forall(i in 1..n)(
            forall(j in i+1..n)(
                abs(q[i]-q[j])!=abs(i-j)
            )
    )
    '''
)

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, nqueens)
# Assign 4 to n
instance["n"] = 4
start_time = time.time()
result = instance.solve()
# Output the array q
print("\n")
print("Resolved in --- %s seconds ---" % (time.time() - start_time))
print(result["q"])


# NQueens all different model
nqueens = Model()
nqueens.add_string(
    '''
    int: n; % The number of queens.

    array [1..n] of var 1..n: q;

    include "alldifferent.mzn";

    constraint alldifferent(q);
    constraint alldifferent(i in 1..n)(q[i] + i);
    constraint alldifferent(i in 1..n)(q[i] - i);
    '''
)

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, nqueens)
# Assign 4 to n
instance["n"] = 4
start_time = time.time()
result = instance.solve()
# Output the array q
print("\n")
print("Resolved in --- %s seconds ---" % (time.time() - start_time))
print(result["q"])
