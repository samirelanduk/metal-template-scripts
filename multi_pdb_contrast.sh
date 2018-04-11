#!/usr/bin/env bash

pdbs=($1'/????.pdb')

for pdb in $pdbs
    do
        name=${pdb%.pdb}
        suffix='_grid.pdb'
        grid="$name$suffix"
        echo; echo; echo;
        echo $name

        ./generate_grid.py $pdb $2 --margin $3 --trim $4 --pad $5

        ./evaluate_contrast.py $pdb $grid
    done
