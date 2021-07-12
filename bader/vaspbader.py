import os
import sys
import pandas as pd
from ase import atoms
from ase.io import read
from ase.visualize import view


if len(sys.argv) != 4 or "-h" in sys.argv or "--help" in sys.argv :
    print("Use of vaspbader.py:")
    print("$ python3 vaspbader.py CONTCAR ACF.dat POTCAR")
    print("Exiting Program")
    print()
    sys.exit()


atoms = read(sys.argv[1])
baderfile = sys.argv[2]
potcarfile = sys.argv[3]


with open(baderfile, "r") as f:
    lines = f.readlines()

nlines = len(lines)
data = []

linecount = 0
for iline in range(0, nlines):

    if linecount == 0:
        header = lines[iline].split()

        header[5] = header[5] + "_" + header[6]
        header[7] = header[7] + "_" + header[8]

        del header[8]
        del header[6]
        del header[0]

    if linecount > 1 and linecount < nlines - 4:
        d = lines[iline].split()
        d[1] = float(d[1])
        d[2] = float(d[2])
        d[3] = float(d[3])
        d[4] = float(d[4])
        d[5] = float(d[5])
        d[6] = float(d[6])

        del d[0]
        data.append(d)

    linecount += 1

zvals = []
with open(potcarfile, "r") as f:
    for line in f:
        if "ZVAL" in line:
            z = line.split()
            zvals.append(float(z[5]))

valence_electrons = []
idx = -1
tmp = " "
for s in atoms.symbols:
    if s != tmp:
        idx += 1
        tmp = s
    valence_electrons.append(zvals[idx])

df = pd.DataFrame(data, columns=header)
df.insert(6, "Atomic_Symbol", atoms.symbols)
df.insert(7, "Valence_Electrons", valence_electrons)
df["Partial_Bader_Charge"] = df["Valence_Electrons"] - df["CHARGE"]

print(df)
view(atoms)
