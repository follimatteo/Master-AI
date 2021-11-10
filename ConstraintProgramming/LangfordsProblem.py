import time
from minizinc import Instance, Model, Solver

# Load n-Queens model from file
seq = Model()
seq.add_string(
    '''
    int: n;
    int: k;

    array[1..(n*k)] of var 1..n: seq;

    constraint
        forall(i in 1..n)(
            sum (j in 1..(n*k))(if seq[j]==i then 1 else 0 endif) == k);

    constraint
        forall(i in 1..n*k)(
            forall(j in i+1..n*k)(
                if seq[i]==seq[j] then j-i-1 == seq[i] endif
            )
        );
    solve satisfy;

    '''
)

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, seq)
# Assign 4 to n
instance["n"] = 15
instance["k"] = 3
start_time = time.time()
result = instance.solve()
print("Resolved in --- %s seconds ---" % (time.time() - start_time))
print(result)
