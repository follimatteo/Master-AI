import imp
import numpy as np
import argparse
import os
from pathlib import Path
import time
from z3 import *
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()

parser.add_argument("-t", "--timeout", help="Timeout in seconds (300 by default)", required=False, type=int)
parser.add_argument("--rotation", dest="rotation", action="store_true")
parser.add_argument(
    "-o", "--out_path", help="path to result output files", default="out"
)
parser.set_defaults(rotation=False)


def main():
    instances = []
    time_spent = []
    args = vars(parser.parse_args())
    for inst in [5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]:

        filename = "src/Instances/{}x{}.txt".format(inst, inst)

        rotation = args["rotation"]
        out_path = args["out_path"]
        rotation = args["rotation"]
        timeout = args["timeout"]

        if os.path.exists(filename):
            print("Solving instance: {}".format(filename[4:]))
            widths = []
            heights = []

            with open(filename, "r") as f:
                lines = f.read().splitlines()
                first_row = lines[0].split(" ")
                W = int(first_row[0])
                H = int(first_row[1])

                for row in lines[2:]:
                    row_contents = row.split(" ")
                    if len(row_contents) > 1:
                        widths.append(int(row_contents[0]))
                        heights.append(int(row_contents[1]))

            N = len(widths)

            sorted_ind = np.argsort(np.array(widths)*np.array(heights))
            sorted_ind = np.flipud(sorted_ind)
            widths = list(np.array(widths)[sorted_ind])
            heights = list(np.array(heights)[sorted_ind])
            widths = [int(w) for w in widths]
            heights = [int(h) for h in heights]

            hor_dim = [z3.Int("width_{}".format(i)) for i in range(N)]
            ver_dim = [z3.Int("height_{}".format(i)) for i in range(N)]

            X = [z3.Int("x_{}".format(i)) for i in range(N)]
            Y = [z3.Int("y_{}".format(i)) for i in range(N)]

            s = z3.Solver()

            
            # Objects are smaller than the roll
            for i in range(N):
                s.add(X[i] >= 0, X[i] + hor_dim[i] <= W)
                s.add(Y[i] >= 0, Y[i] + ver_dim[i] <= H)

            # Non overlapping
            for j in range(N):
                for i in range(j):
                    s.add(
                        z3.Or(
                            X[i] + hor_dim[i] <= X[j],
                            X[j] + hor_dim[j] <= X[i],
                            Y[i] + ver_dim[i] <= Y[j],
                            Y[j] + ver_dim[j] <= Y[i],
                        )
                    )


            for i in range(N):
                if rotation:
                    s.add(
                        z3.Or(
                            z3.And(
                                hor_dim[i] == widths[i], ver_dim[i] == heights[i]
                            ),
                            z3.And(
                                hor_dim[i] == heights[i], ver_dim[i] == widths[i]
                            ),
                        )
                    )
                else:
                    s.add(z3.And(hor_dim[i] == widths[i], ver_dim[i] == heights[i]))

        
            # symmetry breaking
            s.add(
                X[0] <= (W // 2 - hor_dim[0] / 2), Y[0] <= (H // 2 - ver_dim[0] / 2)
            )


            timeout = args["timeout"] * 1000 if args["timeout"] is not None else 300000
            s.set('timeout', timeout)

            before = time.time()
            result = s.check()
            print("The instance is: ", result)
            after = time.time()
            print("Elapsed time {:.2f}s".format(after - before))
            instances.append(inst)
            time_spent.append(after-before)

            if result == sat:
                assignments = s.model()
                # fetch variable assignments individually
                outX = []
                outY = []
                widths = []
                heights = []
                for i in range(N):
                    outX.append(assignments[X[i]])
                    outY.append(assignments[Y[i]])
                    widths.append(assignments[hor_dim[i]])
                    heights.append(assignments[ver_dim[i]])

                exp_directory = out_path
                exp_directory = Path(exp_directory)

                if not exp_directory.exists():
                    exp_directory.mkdir()

                instance_name = filename.split("/")[-1]
                instance_name = instance_name[: len(instance_name) - 4]
                output_filename = os.path.join(exp_directory, instance_name + "-out.txt")

                with open(output_filename, "w") as f:
                    f.write("{} {}\n".format(W, H))
                    f.write("{}\n".format(N))
                    for outputs in zip(widths, heights, outX, outY):
                        f.write("{} {}\t{} {}\n".format(*outputs))

        else:
            print("Error: file {} does not exist.".format(filename[4:]))

    plt.scatter(instances, time_spent)
    plt.title("Time on each instance")
    plt.xlabel("Instances")
    plt.ylabel("Time")
    plt.show()


if __name__ == "__main__":
    main()
