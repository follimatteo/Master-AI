from minizinc import Instance, Model, Solver
import time

NQ = 12
allsol = True
print_result = False

def print_chessboard(chessboard):
    for row in chessboard:
        for el in row:
            if el:
                print('Q', end=' ')
            else:
                print('_', end=' ')
        print()


# NQueens basic resolution
nqueens = Model()
nqueens.add_string(
    '''
    int: n; % The number of queens.

    array[1..n,1..n] of var bool: qb;

    array [1..n] of var 1..n: q;

    include "alldifferent.mzn";

    constraint forall (i,j in 1..n) ( qb[i,j] <-> (q[i]=j) );

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
instance["n"] = NQ
start_time = time.time()
result = instance.solve(all_solutions=allsol)
# Output the array q
print("\n")
print("Resolved in --- %s seconds ---" % (time.time() - start_time))
if allsol:
    print(f'Number of solution: {len(result)}')
    if print_result:
        for i in range(len(result)):
            print(f'Solution: {i+1}')
            print_chessboard(result[i, 'qb'])
            print('\n')
else:
    print_chessboard(result["qb"])


# NQueens all different model
nqueens = Model()
nqueens.add_string(
    '''
    int: n; % The number of queens.

    array[1..n,1..n] of var bool: qb;

    array [1..n] of var 1..n: q;

    include "alldifferent.mzn";

    constraint forall (i,j in 1..n) ( qb[i,j] <-> (q[i]=j) );

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
instance["n"] = NQ
start_time = time.time()
result = instance.solve(all_solutions=allsol)
# Output the array q
print("\n")
print("Resolved in --- %s seconds ---" % (time.time() - start_time))
if allsol:
    print(f'Number of solution: {len(result)}')
    if print_result:
        for i in range(len(result)):
            print(f'Solution: {i+1}')
            print_chessboard(result[i, 'qb'])
            print('\n')
else:
    print_chessboard(result["qb"])

#
#   Breaking simmetry
#   1' : constraint q[1] <= n div 2  ------> THIS FORCE THE QUEEN IN THE FIRST COLUMN TO BE IN THE FIRST HALF, BREAKING VERTICAL SIMMETRY
#   2' : fzn_lex_lesseq_bool([ qb[i,j] | i,j in 1..n ], [ qb[j,i] | i,j in 1..n ])  ----> THIS BREAK SIMMITRY WITH LEXOGRAPIC ORDER RESPECT TO DIAGONAL?
#
#
nqueens = Model()
nqueens.add_string(
    '''
    int: n; % The number of queens.

    array[1..n,1..n] of var bool: qb;

    array [1..n] of var 1..n: q;

    include "alldifferent.mzn";
    include "fzn_lex_lesseq_bool.mzn";

    constraint forall (i,j in 1..n) ( qb[i,j] <-> (q[i]=j) );

    constraint alldifferent(q);
    constraint alldifferent(i in 1..n)(q[i] + i);
    constraint alldifferent(i in 1..n)(q[i] - i);

    %constraint q[1] <= n div 2;
    constraint
        fzn_lex_lesseq_bool(array1d(qb), [ qb[j,i] | i,j in 1..n ])
        /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[i,j] | i in reverse(1..n), j in 1..n ])
        /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[j,i] | i in 1..n, j in reverse(1..n) ])
        /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[i,j] | i in 1..n, j in reverse(1..n) ])
        /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[j,i] | i in reverse(1..n), j in 1..n ])
        /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[i,j] | i,j in reverse(1..n) ])
        /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[j,i] | i,j in reverse(1..n) ]);
    '''
)

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, nqueens)
# Assign 4 to n
instance["n"] = NQ
start_time = time.time()
result = instance.solve(all_solutions=allsol)
# Output the array q
print("\n")
print("Resolved in --- %s seconds ---" % (time.time() - start_time))
if allsol:
    print(f'Number of solution: {len(result)}')
    if print_result:
        for i in range(len(result)):
            print(f'Solution: {i+1}')
            print_chessboard(result[i, 'qb'])
            print('\n')
else:
    print_chessboard(result["qb"])
