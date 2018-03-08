#! /usr/bin/env python3

import atomium
import sys
from tqdm import tqdm

if len(sys.argv) == 1:
    print("Please provide a PDB")
    sys.exit()
pdb = sys.argv[1]
if len(sys.argv) <= 2:
    print("Please provide a grid size")
    sys.exit()
size = float(sys.argv[2])
trim = None
if len(sys.argv) > 3:
    trim = float(sys.argv[3])

# Get the model, either from disk or the server
try:
    model = atomium.pdb_from_file(pdb).model()
except:
    model = atomium.fetch(pdb).model()

# Generate a cuboid grid
grid = model.grid(size=size)

# Should the grid be trimmed to only include those near an atom?
if trim is not None:
    trimmed = []
    print("Trimming grid...")
    for coordinate in tqdm(grid):
        if len(model.atoms_in_sphere(*coordinate, trim)) > 0:
            trimmed.append(coordinate)
    print("{} grid points were trimmed to {} relevant grid points".format(
     len(grid), len(trimmed)
    ))
    grid = trimmed

# Output the grid
lines = [("HETATM" + ((" ") * 24) + str(x).ljust(8) + str(y).ljust(8) + str(z).ljust(8)).ljust(80) + "\n" for x, y, z in grid]
with open(pdb.replace(".pdb", "") + "_grid.pdb", "w") as f:
    f.writelines(lines)
