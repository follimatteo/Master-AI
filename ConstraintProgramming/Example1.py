from minizinc import Instance, Model, Solver

# Load n-Queens model from file
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
result = instance.solve()
# Output the array q
print(result["q"])




'''
EXAMPLE
We know how to make two sorts of cakes (WARNING: please don’t use these recipes at home).
A banana cake which takes 250g of self-raising flour, 2 mashed bananas, 75g sugar and 100g of butter,
and a chocolate cake which takes 200g of self-raising flour, 75g of cocoa, 150g sugar and 150g of butter.
We can sell a chocolate cake for $4.50 and a banana cake for $4.00. And we have 4kg self-raising flour,
6 bananas, 2kg of sugar, 500g of butter and 500g of cocoa. The question is how many of each sort of cake
should we bake for the fete to maximise the profit.
'''

cake = Model()
cake.add_string(
    '''
    var 1..100: n_banana;
    var 1..100: n_choco;

    constraint n_banana*250+n_choco*200 <= 4000;
    constraint n_banana*75+n_choco*150 <= 2000;
    constraint n_banana*100+n_choco*150 <= 500;
    constraint n_choco*75 <= 500;
    constraint n_banana*2 <= 6;

    solve maximize 450*n_banana+400*n_choco;
    '''
)

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, cake)
result = instance.solve()
# Output the array q
print(result)


model = Model()
model.add_string(
    """
    include "all_different.mzn";
    set of int: A;
    set of int: B;
    array[A] of var B: arr;
    var set of B: X;
    var set of B: Y;

    constraint all_different(arr);
    constraint forall (i in index_set(arr)) ( arr[i] in X );
    constraint forall (i in index_set(arr)) ( (arr[i] mod 2 = 0) <-> arr[i] in Y );

    """
)

instance = Instance(gecode, model)
instance["A"] = range(3, 8)  # MiniZinc: 3..8
instance["B"] = {4, 3, 2, 1, 0}  # MiniZinc: {4, 3, 2, 1, 0}

result = instance.solve()
print(result["X"])  # range(0, 5)
assert isinstance(result["X"], range)
print(result["Y"])  # {0, 2, 4}
assert isinstance(result["Y"], set)


'''
8 Nodes, for every adjacent node |Ni-Nj|>1
'''

node = Model()
node.add_string(
    '''
    include "alldifferent.mzn";

    set of int: DIGIT = 0..9;
    var DIGIT: N1;
    var DIGIT: N2;
    var DIGIT: N3;
    var DIGIT: N4;
    var DIGIT: N5;
    var DIGIT: N6;
    var DIGIT: N7;
    var DIGIT: N8;

    constraint alldifferent([N1, N2, N3, N4, N5, N6, N7, N8]);
    constraint abs(N1-N2)>1;
    constraint abs(N1-N4)>1;
    constraint abs(N1-N3)>1;
    constraint abs(N2-N5)>1;
    constraint abs(N2-N3)>1;
    constraint abs(N3-N4)>1;
    constraint abs(N3-N5)>1;
    constraint abs(N3-N6)>1;
    constraint abs(N3-N7)>1;
    constraint abs(N4-N6)>1;
    constraint abs(N4-N7)>1;
    constraint abs(N5-N6)>1;
    constraint abs(N5-N8)>1;
    constraint abs(N6-N7)>1;
    constraint abs(N6-N8)>1;
    constraint abs(N7-N8)>1;
    '''
)

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, node)
result = instance.solve(all_solutions=True)
# Output the array q
for sol in result.solution:
    print(sol)
