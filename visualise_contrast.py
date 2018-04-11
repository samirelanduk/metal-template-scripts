#! /usr/bin/env python3

import sys

if len(sys.argv) == 1:
    print("Please provide a contrast data file")
    sys.exit()
contrast = sys.argv[1]
if len(sys.argv) == 2:
    print("How many data points to show?")
    sys.exit()
point_count = int(sys.argv[2])

# Open data file
with open(contrast) as f:
    lines = f.read().splitlines()[1:]
data = [[float(val) for val in line.split()] for line in lines]

# Should be sorted anyway but just in case
data = sorted(data, key=lambda l: l[-1])

# Ouptut the relevant points to PDB
points = [line[:3] for line in data[-point_count:]]
lines = [("HETATM" + ((" ") * 24) + str(x).ljust(8) + str(y).ljust(8)
 + str(z).ljust(8)).ljust(80) + "\n" for x, y, z in points]
with open("{}_best_{}.pdb".format(contrast.replace(".dat", ""), point_count), "w") as f:
    f.writelines(lines)
