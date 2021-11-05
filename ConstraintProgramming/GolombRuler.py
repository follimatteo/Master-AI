from minizinc import Instance, Model, Solver

# Load n-Queens model from file
rulers = Model()
rulers.add_string(
    '''
    int: n; % The number of queens.

    array [1..n] of var 0..2^(n-1): q;

    include "alldifferent.mzn";

    constraint alldifferent(q);
    constraint forall(i in 1..(n-1))(q[i]<q[i+1]);
    constraint alldifferent([q[i]-q[j]|i,j in 1..n where i<j]);

    solve minimize max(q);
    '''
)
#constraint alldifferent(i in 1..(n-1), j in (i+1)..n)(q[i]+q[j]);


# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, rulers)
# Assign 4 to n
instance["n"] = 28
result = instance.solve()
print(result)
