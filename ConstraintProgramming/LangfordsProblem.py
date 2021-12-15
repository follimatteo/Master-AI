import time
from minizinc import Instance, Model, Solver

import argparse

parser = argparse.ArgumentParser(description="Langford's Problem solver with MiniZinc solver")
parser.add_argument('N', nargs='?', type=int, default=4)
parser.add_argument('K', nargs='?', type=int, default=2, help="occurrence for each number")

args = parser.parse_args()

n = args.N
k = args.K

seq = Model()
seq.add_string(
    '''
    include "alldifferent.mzn";

    int: n;
    int: k;

    %%% matrix i number j occurrence
    array[1..n,1..k] of var 1..n*k: seq;

    constraint
        alldifferent(seq);

    constraint
        forall(i in 1..n)(
            forall(j in 1..k-1)(
                seq[i,j+1] == i+1+seq[i,j]
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
instance["n"] = n
instance["k"] = k
start_time = time.time()
result = instance.solve()
print("Resolved in --- %s seconds ---" % (time.time() - start_time))
print(result)


#
seq = Model()
seq.add_string(
    '''
    int: n;
    int: k;

    array[1..(n*k)] of var 1..n: seq;

    %% this check that each number is inside the seq exacly k times

    constraint
        forall(i in 1..n)(
            sum (j in 1..(n*k))(if seq[j]==i then 1 else 0 endif) == k);

    %% check that distance between number is number itself

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
instance["n"] = n
instance["k"] = k
start_time = time.time()
result = instance.solve()
print("Resolved in --- %s seconds ---" % (time.time() - start_time))
print(result)
