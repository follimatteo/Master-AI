
import time
import argparse
from util import txt_to_data, print_history, load_model, evaluate_model
import os


timeout = 300

model_p = 'Model/Model2.txt'
data_p = 'Instances/'

files = os.listdir(data_p)

size = []
time = []
fail = []

for i, f in enumerate(files):

    print(f'Working on model {i}')
    print('\n')

    model = load_model(model_p)
    data = txt_to_data(data_p+f)

    r = evaluate_model(model, data)



    size.append(int(f[:2]))
    time.append(r.statistics['solveTime'].total_seconds())
    fail.append(r.statistics['failures'])

    if time[-1]>timeout-10:
        break

print(size)
print(time)
print(fail)
print_history(size, time, fail)
