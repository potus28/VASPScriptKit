import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from ase.io import read, write
from ase.build import molecule
from ase.calculators.vasp import Vasp
mpl.style.use("seaborn-poster")

infile = sys.argv[1]
uc = read(infile)

encuts = [400, 425, 450, 475, 500, 525, 550, 600, 700]
kpts = 4
TE = []


for e in encuts:
	calc = Vasp(
		directory='uc-encut-{0}'.format(e),
		xc='PBE',
		kpts=[kpts, kpts, kpts],
		encut=e,
		atoms=uc)

	TE.append(uc.get_potential_energy())
	
	if None in TE:
		calc.abort()

# consider the change in energy from lowest energy state
TE = np.array(TE)
TE -= TE.min()

print(encuts)
print(TE)

plt.plot(KPTS, TE)
plt.xlabel('Energy Cutoff (eV)')
plt.ylabel('Total Energy (eV)')
plt.savefig('uc-encut-convergence.png')

