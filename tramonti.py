import sys, os
import numpy as np
import argparse
import matplotlib.pyplot as plt
import scipy
import decimal

sys.path.append('funzioni.py')
import funzioni

T_s  = 5.75e3 # K	
T_a  = 4e3    # K
T_sp = 18e3   # K

#numero di fotoni
N_fot=1000
lmax = 2e-6
lmin = 1e-7
ld=np.linspace(lmin,lmax,N_fot)


mc_int=(lmax-lmin)/N_fot * somma

