#! /usr/bin/env python3

import atomium
import sys
from tqdm import tqdm
import multiprocessing
from multiprocessing import Pool

if len(sys.argv) == 1:
    print("Please provide a PDB")
    sys.exit()
pdb = sys.argv[1]
if len(sys.argv) <= 2:
    print("Please provide a grid size")
    sys.exit()
size = float(sys.argv[2])

margin = 0
if "--margin" in sys.argv:
    margin = float(sys.argv[sys.argv.index("--margin") + 1])

trim = None
if "--trim" in sys.argv:
    trim = float(sys.argv[sys.argv.index("--trim") + 1])

pad = None
if "--pad" in sys.argv:
    pad = float(sys.argv[sys.argv.index("--pad") + 1])

# Get the model, either from disk or the server
try:
    model = atomium.pdb_from_file(pdb).model
except:
    model = atomium.fetch(pdb).model

# Generate a cuboid grid
grid = list(model.grid(size=size, margin=margin))

# Should the grid be trimmed to only include those near an atom?
if trim is not None:

    def check_point(point):
        atoms_in_sphere = model.atoms_in_sphere(*point, trim, metal=False)
        return (point if len(atoms_in_sphere) > 0 else None)

    print("Trimming grid...")
    with Pool() as p:
        trimmed = list(tqdm(p.imap(check_point, grid), total=len(grid)))

    trimmed = list(filter(bool, trimmed))
    print("{} grid points were trimmed to {} relevant grid points".format(
     len(grid), len(trimmed)
    ))
    grid = trimmed


# Should the grid be have points too close to an atom removed?
if pad is not None:

    def check_point(point):
        atoms_in_sphere = model.atoms_in_sphere(*point, pad, metal=False)
        return (point if len(atoms_in_sphere) == 0 else None)

    print("Removing clashing grid points...")
    with Pool() as p:
        trimmed = list(tqdm(p.imap(check_point, grid), total=len(grid)))

    trimmed = list(filter(bool, trimmed))
    print("{} grid points were reduced to {} relevant grid points".format(
     len(grid), len(trimmed)
    ))
    grid = trimmed

# Output the grid
lines = [("HETATM" + ((" ") * 24) + str(x).ljust(8) + str(y).ljust(8)
 + str(z).ljust(8)).ljust(80) + "\n" for x, y, z in grid]
with open(pdb.replace(".pdb", "") + "_grid.pdb", "w") as f:
    f.writelines(lines)
