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
N_fot=10000
N_estr=10000
lmax = 2e-6
lmin = 1e-7
lt=np.linspace(lmin,lmax,N_estr)
ld=np.random.uniform(lmin,lmax,N_estr)

def scaled_den(l,T):
	return funzioni.den_fot(l,T)/max(funzioni.den_fot(l,T))
	
y_i = np.random.random(N_estr)
	
mask= y_i <= scaled_den(ld, T_s)

x_i=ld[mask]

plt.hist(x_i,bins=100,color='blue',ec='darkblue')
plt.suptitle('distribuzione dei fotoni che arrivano in caso di non assorbimento')
plt.show()	

