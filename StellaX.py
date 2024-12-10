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
theta = 13*np.pi/36 # angolo zenitale (65°)
R_ter = 6.378e6  #m Raggio della Terra 
lo    = X_st['lambda (nm)'] 
ld    = lo*10**(-9)
ph    = X_st['photons']
n_ter = 1.00029  # indice di rifrazione dell'aria
N_ter = 2.504e25 # mol/m^3

m_p=max(ph)
den_abs = ph/m_p #densità dei fotoni (dati del file)

#stampo i nomi delle colonne del file
print(X_st.columns)

plt.plot(ld, den_abs, 'o', color='royalblue')
plt.xlabel(r'$\lambda$ (nm)')
plt.ylabel('den_fotoni')
plt.show()


def fit_fun(x, T):
	"""
	funzione con la quale faremo il fit dei dati forniti dal file
	per poter calcolare il valore della temperatura della stella X
	"""
	s = fu.th_airmass(R_ter, 8000, theta)
	beta = fu.beta_sc(x, n_ter, N_ter)
	return fu.den_fot(x,T) * np.exp(-beta * s)/max(fu.den_fot(x,T) * np.exp(-beta * s))

pstart=np.array([18e3])
p, pcov = optimize.curve_fit(fit_fun, ld, den_abs, p0=pstart)
print('temperatura ricavata attraverso il fit della stella:', p)
y = fit_fun(ld, p)
plt.subplots(figsize=(9,6))

#test del chi2
chi2 = np.sum((y-den_abs)**2 /den_abs)
ndf  = len(ld)-len(p)
print("\u03C7^2 / ndf = ",chi2/ndf )

plt.plot(ld, den_abs, 'o', color='royalblue', label='punti del file')
plt.plot(ld, y, color='limegreen', label='curva del fit')
plt.xlabel(r'$\lambda$ (nm)')
plt.ylabel('densità fotoni')
plt.text(2e-6,0.8, 'T={:}'.format(p[0]), fontsize=16)
plt.suptitle('fit dei punti forniti')

plt.legend()
plt.show()


