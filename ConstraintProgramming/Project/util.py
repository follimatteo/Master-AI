from minizinc import Instance, Model, Solver
from datetime import timedelta
import matplotlib.pyplot as plt

def txt_to_data(file_name):
    data = {}

    f = open(file_name, "r")
    line = f.readline().split()
    data['W'] = int(line[0])
    data['H'] = int(line[1])

    line = f.readline()
    data['n'] = int(line)

    dx = []
    dy = []
    for i in range(int(line)):
        line = f.readline().split()
        dx.append(int(line[0]))
        dy.append(int(line[1]))

    data['dx'] = dx
    data['dy'] = dy

    f.close()
    return data


def load_model(file_name):

    f = open(file_name, "r")
    model = f.read()

    f.close()

    return model

def print_sol(data, result):

    x = list(range(data['W']+1))
    y = list(range(data['H']+1))

    fig, ax = plt.subplots()
    ax.pcolormesh(x, y, result)
    plt.show()


def evaluate_model(model, data, allsol = False, timeout = 300):

    PWP = Model()

    PWP.add_string(
        model
     )
    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("gecode")
     # Create an Instance of the n-Queens model for Gecode
    instance = Instance(gecode, PWP)
    # Assign 4 to n
    instance["W"] = data['W']
    instance["H"] = data['H']
    instance["n"] = data['n']
    instance["dx"] = data['dx']
    instance["dy"] = data['dy']

    result = instance.solve(all_solutions=allsol, timeout = timedelta(seconds=timeout))

    return result

def print_history(size, time, failures):

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('Evaluation history:')

    ax1.plot(size, time, '.-')
    ax1.set_ylabel('Time (s):')

    ax2.plot(size, failures, '.-')
    ax2.set_xlabel('Box size (NxN):')
    ax2.set_ylabel('Number of failures:')

    plt.show()
