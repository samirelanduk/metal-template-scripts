#! /usr/bin/env python3

import atomium
import biometal
import sys
from tqdm import tqdm
import multiprocessing
from multiprocessing import Pool

if len(sys.argv) == 1:
    print("Please provide a PDB")
    sys.exit()
pdb = sys.argv[1]
if len(sys.argv) <= 2:
    print("Please provide a grid")
    sys.exit()
grid = sys.argv[2]

# Get the model, either from disk or the server
try:
    model = atomium.pdb_from_file(pdb).model
except:
    model = atomium.fetch(pdb).model

# Get the grid coordinates
data_file = atomium.pdb_data_from_file(grid)
grid = [(a["x"], a["y"], a["z"]) for a in data_file["models"][0]["molecules"][0]["atoms"]]
print("There are {} grid points to evaluate".format(len(grid)))

# Evaluate at all grid points
def check_point(point):
    c_35 = biometal.hydrophobic_contrast(model, *point, 3.5, metal=False)
    c_7 = biometal.hydrophobic_contrast(model, *point, 7, metal=False)
    return (*point, c_35, c_7)

print("Evaluating C...")
with Pool() as p:
    scores = list(tqdm(p.imap(check_point, grid), total=len(grid)))

max_35, max_70 = max([s[3] for s in scores]), max([s[4] for s in scores])
scale = max_35 / max_70 if max_70 else 1

scores = [score + ((score[3] + (scale * score[4])),) for score in scores]
scores = sorted(scores, key=lambda s: s[-1])
lines = ["".join([str(round(val, 3)).ljust(11) for val in score]) + "\n" for score in scores]
lines.insert(0, "x          y         z          C_3.5      c_7.0       score\n")
with open(pdb.replace(".pdb", "") + "_scores.dat", "w") as f:
    f.writelines(lines)
