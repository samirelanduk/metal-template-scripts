#! /usr/bin/env python3

import atomium

pdbs = ["1TON", "2CAB", "8TLN", "5CPA", "7ADH"]

sites = {}
for pdb in pdbs:
    print(f"Processing {pdb}...")
    model = atomium.fetch(pdb).model()
    zincs = model.atoms(element="ZN")
    print(f"  Found {len(zincs)} zinc atom" + ("s" if len(zincs) != 1 else ""))
    for zinc in zincs:
        id_ = pdb + zinc.molecule().molecule_id()
        site = zinc.molecule().site()
        site.add_atom(zinc)
        site.translate(-zinc.x(), -zinc.y(), -zinc.z())
        sites[id_] = site
        print(f"  Extracting {id_}...")

print(f"Saving {len(sites)} zinc sites as PDBs...")
for site in sites:
    sites[site].save(f"{site}.pdb")
