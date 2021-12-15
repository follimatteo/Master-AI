from minizinc import Instance, Model, Solver
import time
from datetime import timedelta
import argparse

parser = argparse.ArgumentParser(description='Nqueens Problem solver with MiniZinc solver')
parser.add_argument('N', nargs='?', type=int, default=5)
parser.add_argument('--models', nargs='*', default='all', help="choose between ['raw', 'alldiff', 'sym'] or default 'all' ")
parser.add_argument('--all_solutions',  default=False, help='if FALSE stop at the first solution')
parser.add_argument('--print_board',  default=False, help='if TRUE print all the results board')
parser.add_argument('--timeout', nargs='?', type=int, default=None)
args = parser.parse_args()

print(args)
NQ = args.N
allsol = args.all_solutions
print_board = args.print_board
MODELS = args.models
timeout = timedelta(seconds=args.timeout)

def print_chessboard(chessboard):
    for row in chessboard:
        for el in row:
            if el:
                print('Q', end=' ')
            else:
                print('_', end=' ')
        print()


# NQueens basic resolution
if 'raw' in MODELS or MODELS =='all':
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
        );
        '''
    )

    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("gecode")
    # Create an Instance of the n-Queens model for Gecode
    instance = Instance(gecode, nqueens)
    # Assign 4 to n
    instance["n"] = NQ
    start_time = time.time()
    result = instance.solve(all_solutions=allsol, timeout = timeout)
    # Output the array q
    print("\n")
    print("Raw model:")
    print("Resolved in --- %s seconds ---" % (time.time() - start_time))
    if allsol:
        print(f'Number of solution: {len(result)}')
        if print_board:
            for i in range(len(result)):
                print(f'Solution: {i+1}')
                print_chessboard(result[i, 'qb'])
                print('\n')
    else:
        if print_board:
            print_chessboard(result["qb"])


# NQueens all different model
if 'alldiff' in MODELS or MODELS =='all':
    nqueens = Model()
    nqueens.add_string(
        '''
        include "alldifferent.mzn";

        int: n;
        array [1..n] of var 1..n: q; % queen in column i is in row q[i]

        include "alldifferent.mzn";

        constraint alldifferent(q);                       % distinct rows
        constraint alldifferent([ q[i] + i | i in 1..n]); % distinct diagonals
        constraint alldifferent([ q[i] - i | i in 1..n]); % upwards+downwards

        % search
        solve :: int_search(q, dom_w_deg, indomain_min) satisfy;
        '''
    )

    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("gecode")
    # Create an Instance of the n-Queens model for Gecode
    instance = Instance(gecode, nqueens)
    # Assign 4 to n
    instance["n"] = NQ
    start_time = time.time()
    result = instance.solve(all_solutions=allsol, timeout = timeout)
    # Output the array q
    print("\n")
    print("Alldiff model:")
    print("Resolved in --- %s seconds ---" % (time.time() - start_time))
    if allsol:
        print(f'Number of solution: {len(result)}')
        if print_board:
            for i in range(len(result)):
                print(f'Solution: {i+1}')
                print_chessboard(result[i, 'q'])
                print('\n')
    else:
        if print_board:
            print_chessboard(result["q"])

#
#   Breaking simmetry
#   1' : constraint q[1] <= n div 2  ------> THIS FORCE THE QUEEN IN THE FIRST COLUMN TO BE IN THE FIRST HALF, BREAKING VERTICAL SIMMETRY
#   2' : fzn_lex_lesseq_bool([ qb[i,j] | i,j in 1..n ], [ qb[j,i] | i,j in 1..n ])  ----> THIS BREAK SIMMITRY WITH LEXOGRAPIC ORDER RESPECT TO DIAGONAL?
#
#

if 'sym' in MODELS or MODELS =='all':
    nqueens = Model()
    nqueens.add_string(
        f'''
        int: n; % The number of queens.

        array[1..n,1..n] of var bool: qb;

        array [1..n] of var 1..n: q;

        include "alldifferent.mzn";
        include "fzn_lex_lesseq_bool.mzn";

        constraint forall (i,j in 1..n) ( qb[i,j] <-> (q[i]=j) );

        constraint alldifferent(q);
        constraint alldifferent(i in 1..n)(q[i] + i);
        constraint alldifferent(i in 1..n)(q[i] - i);

        constraint
            fzn_lex_lesseq_bool(array1d(qb), [ qb[j,i] | i,j in 1..n ])
            /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[i,j] | i in reverse(1..n), j in 1..n ])
            /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[j,i] | i in 1..n, j in reverse(1..n) ])
            /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[i,j] | i in 1..n, j in reverse(1..n) ])
            /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[j,i] | i in reverse(1..n), j in 1..n ])
            /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[i,j] | i,j in reverse(1..n) ])
            /\  fzn_lex_lesseq_bool(array1d(qb), [ qb[j,i] | i,j in reverse(1..n) ]);

        solve :: int_search(qb, input_order, indomain_min) satisfy;
        '''
    )

    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("gecode")
    # Create an Instance of the n-Queens model for Gecode
    instance = Instance(gecode, nqueens)
    # Assign 4 to n
    instance["n"] = NQ
    start_time = time.time()
    result = instance.solve(all_solutions=allsol, timeout = timeout)
    # Output the array q
    print("\n")
    print("Sym breaking model:")
    print("Resolved in --- %s seconds ---" % (time.time() - start_time))
    if allsol:
        print(f'Number of solution: {len(result)}')
        if print_board:
            for i in range(len(result)):
                print(f'Solution: {i+1}')
                print_chessboard(result[i, 'qb'])
                print('\n')
    else:
        if print_board:
            print_chessboard(result["qb"])
