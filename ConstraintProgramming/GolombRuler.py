import time
from minizinc import Instance, Model, Solver

# Load n-Queens model from file
rulers = Model()
rulers.add_string(
    '''
    int: n; % The number of queens.

    array [1..n] of var 0..2^(n-1): q;

    include "alldifferent.mzn";

    %constraint q[1]= 0;
    constraint alldifferent(q);
    constraint forall(i in 1..(n-1))(q[i]<q[i+1]);
    constraint alldifferent([q[i]-q[j]|i,j in 1..n where i<j]);

    solve minimize max(q);
    '''
)

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, rulers)
# Assign 4 to n
instance["n"] = 15
start_time = time.time()
result = instance.solve()
print("Resolved in --- %s seconds ---" % (time.time() - start_time))
print(result)
