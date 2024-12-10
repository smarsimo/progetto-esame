import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import optimize

sys.path.append('funzioni.py')
import funzioni as fu

X_st  = pd.read_csv('202302/observed_starX.csv')
theta = 65       #°
R_ter = 6.378e6  #m Raggio della Terra 
lo    = X_st['lambda (nm)']
ph    = X_st['photons']
n_ter = 1.00029  # indice di rifrazione dell'aria
N_ter = 2.504e25 # mol/m^3

#stampo i nomi delle colonne del file
print(X_st.columns)
plt.plot(lo, ph, 'o', color='royalblue')
plt.xlabel(r'$\lambda$ (nm)')
plt.ylabel('fotoni')
plt.show()

def fit_fun(x, N_0, T):
	"""
	funzione con cui devo interpolare i dati raccolti
	all'interno del file fornito observed_starX.csv
	"""
	S=fu.th_airmass(R_ter, 8000, theta)
	den = fu.den_fot(x, T)
	return N_0*den*np.exp(-fu.beta_sc(x,n_ter,N_ter) * S)

pstart=([0,0])
p, pcov = optimize.curve_fit(fit_fun, lo, ph, p0=pstart)
y = fit_fun(lo, p[0], p[1])
print(y)
