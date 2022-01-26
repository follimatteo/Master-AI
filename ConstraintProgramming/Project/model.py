
import time
import argparse
from util import txt_to_data, print_history, load_model, evaluate_model, write_sol
import os


parser = argparse.ArgumentParser(description='Wrapping problem')
parser.add_argument('--timeout', nargs='?', type=int, default=300)
parser.add_argument('--instances', nargs='?', type=int, default=0, help="0 for all, n for the NxN model")
parser.add_argument('--models', nargs='?', type=int, default=0, help="0, 1 , 2, 3")
parser.add_argument('--print_sol',  default=False, help='if TRUE print all the results board')
parser.add_argument('--all_sol',  default=False, help='if TRUE find all the possible solution')

args = parser.parse_args()
timeout = args.timeout
model = args.models
p_sol = args.print_sol
all_sol = args.all_sol



### Param
write_out = True ### true to generate the output file
model_p = f'Model/Model{model}.txt'
data_p = 'Instances/'
files = os.listdir(data_p)
insta = args.instances

if insta!=0:
    files = [files[insta-8]]

size = []
time = []
fail = []

for i, f in enumerate(files):
    print('\n')
    print(f'Working with size: {f[:2]}')


    model = load_model(model_p)
    data = txt_to_data(data_p+f)

    r = evaluate_model(model, data, all_sol,  timeout, p_sol)
    
    if r.solution!=None:
        data['ox'] = r.solution.ox
        data['oy'] = r.solution.oy

    size.append(int(f[:2]))
    time.append(r.statistics['solveTime'].total_seconds())
    fail.append(r.statistics['failures'])

    if write_out and r.solution!=None:
        write_sol('out/', f, data)

    if time[-1]>timeout:
        break

print(size)
print(time)
print(fail)
print_history(size, time, fail)
