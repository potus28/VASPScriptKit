import os

# Since we are running vasp are running vasp
# Assume VTST Scripts and the bader program are installed and are somewhere in the PATH
workdir = sys.argv[1]
cmd = "cd "+workdir

os.system(cmd)
os.system("chgsum.pl AECCAR0 AECCAR2")
os.system("bader CHGCAR -ref CHGCAR_sum")111

