import sys,os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import optimize
import warnings

sys.path.append('funzioni.py')
import funzioni as fu

warnings.filterwarnings('ignore')

X_st  = pd.read_csv('202302/observed_starX.csv')
theta = 65#° angolo zenitale
R_ter = 6.378e6  #m Raggio della Terra 
lo    = X_st['lambda (nm)'] 
ld    = lo*10**(-9)
ph    = X_st['photons']
n_ter = 1.00029  # indice di rifrazione dell'aria
N_ter = 2.504e25 # mol/m^3


m_p=max(ph)
den_abs = ph/m_p
print(m_p)
#stampo i nomi delle colonne del file
print(X_st.columns)
print(ld)
plt.plot(ld, den_abs, 'o', color='royalblue')
plt.xlabel(r'$\lambda$ (nm)')
plt.ylabel('den_fotoni')
plt.show()

def fit_fun(x, T, n):
	"""
	funzione con la quale faremo il fit dei dati forniti dal file
	per poter calcolare il valore della temperatura della stella X
	"""
	S    = fu.th_airmass(R_ter, 8000, theta)
	beta = fu.beta_sc(x, n, N_ter)
	return fu.den_fot(x,T) * np.exp(-beta * S)/max(fu.den_fot(x,T) * np.exp(-beta * S))

pstart=np.array([18e3,1])
p, pcov = optimize.curve_fit(fit_fun, ld, den_abs, p0=pstart)
print(p)
y = fit_fun(ld, p[0], p[1])
plt.subplots(figsize=(9,6))
print(y, den_abs)
plt.plot(ld, den_abs, 'o', color='royalblue', label='punti del file')
plt.plot(ld, y, color='limegreen', label='curva del fit')
plt.legend()
plt.show()


