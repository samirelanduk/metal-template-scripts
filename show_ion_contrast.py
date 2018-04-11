#! /usr/bin/env python3

import atomium
import biometal
import sys
import matplotlib.pyplot as plt

if len(sys.argv) == 1:
    print("Please provide a PDB and ion")
    sys.exit()

pdbs = []
for arg in sys.argv[1:-2]:
    pdb, atom_id = arg.split(":")
    model = atomium.pdb_from_file(pdb + ".pdb").model
    pdbs.append({
     "model": model, "atom": model.atom(id=int(atom_id))
    })
radius = float(sys.argv[-2])
step = float(sys.argv[-1])

x = [0.5]
while x[-1] < radius:
    x.append(round(x[-1] + step, 6))

ys = []
for pdb in pdbs:
    ys.append([biometal.hydrophobic_contrast(
     pdb["model"], *pdb["atom"].location, radius, metal=False, pc=False
    ) / 1000 for radius in x])

y = [sum(values) / len(values) for values in zip(*ys)]
y = [val if val or y[index - 1] else None for index, val in enumerate(y)]

plt.plot(x, y)
if len(ys) > 1:
    for i, y_ in enumerate(ys):
        plt.plot(x, y_, linewidth=1, alpha=0.3, label=sys.argv[i + 1][2:])
plt.xlim([0, radius])
if len(ys) > 1: plt.legend()
plt.title("$Zn^{2+}$")
plt.xlabel("R, Å")
plt.ylabel(r"$C,  kcal \cdot mol^{-1}$")
plt.show()
