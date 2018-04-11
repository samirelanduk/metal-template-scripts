#! /usr/bin/env python3

import sys
import os
import atomium

if len(sys.argv) == 1:
    print("Where is the data?")
    sys.exit()
location = sys.argv[1]

files = os.listdir(location)
scores = [f for f in files if f.endswith("_scores.dat")]
os.chdir(location)

print("There are {} PDBs with scores".format(len(scores)))

print("PDB\tPoints\tIon\tRank\tDev.\tScore\tRange")
for scores_file in scores:
    pdb_file = scores_file.replace("_scores.dat", ".pdb")

    with open(scores_file) as f:
        lines = f.read().splitlines()
    lines = [[float(val) for val in line.split()] for line in lines[1:]]
    point_count = len(lines) - 1

    model = atomium.pdb_from_file(pdb_file).model
    metals = model.atoms() - model.atoms(metal=False)
    for i, metal in enumerate(metals):

        point = [line for line in lines if metal.distance_to(line[:3]) <= 3][-1]
        deviation = metal.distance_to(point[:3])
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}{}{}".format(
         pdb_file[:-4] if i == 0 else "",
         point_count if i == 0 else "",
         metal.element,
         len(lines) - lines.index(point),
         round(deviation, 1),
         round(point[-1] / 1000, 1),
         round(max([l[-1] for l in lines]) / 1000, 1) if i == 0 else "",
         "/" if i == 0 else "",
         round(min([l[-1] for l in lines]) / 1000, 1) if i == 0 else ""
        ))
