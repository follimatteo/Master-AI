import numpy as np
import argparse
import os
from pathlib import Path
import time
import z3

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--in_path",
    help="Path to the file containing the input instance",
    required=True,
    type=str,
)
parser.add_argument("--rotation", dest="rotation", action="store_true")
parser.add_argument(
    "-o", "--out_path", help="path to result output file", default="-out.txt"
)
parser.set_defaults(rotation=False)



def main():
    args = vars(parser.parse_args())

    filename = args["in_path"]
    rotation = args["rotation"]
    out_path = args["out_path"]

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

        widths_var = [z3.Int("width_{}".format(i)) for i in range(N)]
        heights_var = [z3.Int("height_{}".format(i)) for i in range(N)]

        X = [z3.Int("x_{}".format(i)) for i in range(N)]
        Y = [z3.Int("y_{}".format(i)) for i in range(N)]

        s = z3.Solver()

        for i in range(N):
            if rotation:
                s.add(
                    z3.Or(
                        z3.And(
                            widths_var[i] == widths[i], heights_var[i] == heights[i]
                        ),
                        z3.And(
                            widths_var[i] == heights[i], heights_var[i] == widths[i]
                        ),
                    )
                )
            else:
                s.add(z3.And(widths_var[i] == widths[i], heights_var[i] == heights[i]))

        # Objects smaller than the roll
        for i in range(N):
            s.add(X[i] >= 0, X[i] + widths_var[i] <= W)
            s.add(Y[i] >= 0, Y[i] + heights_var[i] <= H)

        # Non overlapping
        for j in range(N):
            for i in range(j):
                s.add(
                    z3.Or(
                        X[i] + widths_var[i] <= X[j],
                        X[j] + widths_var[j] <= X[i],
                        Y[i] + heights_var[i] <= Y[j],
                        Y[j] + heights_var[j] <= Y[i],
                    )
                )

        # symmetry breaking
        s.add(
            X[0] <= (W // 2 - widths_var[0] / 2), Y[0] <= (H // 2 - heights_var[0] / 2)
        )

        before = time.time()
        print("The instance is: ", s.check())
        after = time.time()
        print("Elapsed time {:.2f}s".format(after - before))
        assignments = s.model()
        # fetch variable assignments individually
        outX = []
        outY = []
        widths = []
        heights = []
        for i in range(N):
            outX.append(assignments[X[i]])
            outY.append(assignments[Y[i]])
            widths.append(assignments[widths_var[i]])
            heights.append(assignments[heights_var[i]])

        exp_directory = "out1"
        exp_directory = Path(exp_directory)

        if not exp_directory.exists():
            exp_directory.mkdir()

        instance_name = filename.split("/")[-1]
        instance_name = instance_name[: len(instance_name) - 4]
        output_filename = os.path.join(exp_directory, instance_name + out_path)

        with open(output_filename, "w") as f:
            f.write("{} {}\n".format(W, H))
            f.write("{}\n".format(N))
            for outputs in zip(widths, heights, outX, outY):
                f.write("{} {}\t{} {}\n".format(*outputs))

    else:
        print("Error: file {} does not exist.".format(filename[4:]))


if __name__ == "__main__":
    main()
