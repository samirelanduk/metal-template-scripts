#! /usr/bin/env python3

import atomium
import biometal
import sys
import matplotlib.pyplot as plt

if len(sys.argv) == 1:
    print("Please provide a PDB and ion")
    sys.exit()

# Get model and atom for each PDB
pdbs = []
for arg in sys.argv[1:-2]:
    print("Processing", arg)
    pdb, atom_id = arg.split(":")
    model = atomium.pdb_from_file(pdb + ".pdb").model()
    pdbs.append({
     "model": model, "atom": model.atom(atom_id=int(atom_id))
    })
radius = float(sys.argv[-2])
step = float(sys.argv[-1])

x = [2.1, 2.4, 2.7, 3]
while x[-1] < radius:
    x.append(round(x[-1] + step, 6))

ys = []
for pdb in pdbs:
    ys.append([biometal.solvation(
     pdb["model"], *pdb["atom"].location(), radius, het=False
    ) for radius in x])

y = [sum(values) / len(values) for values in zip(*ys)]
y = [val if val or y[index - 1] else None for index, val in enumerate(y)]

plt.plot(x, y)
for i, y_ in enumerate(ys):
    plt.plot(x, y_, linewidth=1, alpha=0.3, label=sys.argv[i + 1][2:])
plt.plot([0, radius], [0, 0], "--", linewidth=1, color="#000000")
plt.plot([0, radius], [7, 7], "--", linewidth=1, alpha=0.2, color="#000000")
plt.xlim([0, radius])
plt.ylim([-30, 10])
plt.legend()
plt.yticks([-30, -20, -10, 0, 10])
plt.show()
