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
ld    = lo*10**(-9) #m
ph    = X_st['photons']
n_ter = 1.00029  # indice di rifrazione dell'aria
N_ter = 2.504e25 # mol/m^3

#divido l'array contenente il numero di fotoni per il valore massimo
#contenuto nell'array stesso in modo da ricavare una densità "osservata"
m_p=max(ph)
den_abs = ph/m_p #densità dei fotoni (dati del file)

#stampo i nomi delle colonne del file
print(X_st.columns)

plt.plot(ld, den_abs, 'o', color='royalblue')
plt.xlabel(r'$\lambda$ (nm)')
plt.ylabel('den_fotoni')
#plt.savefig('immagini/grafico_dati_osservati.jpeg')
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

error=np.sqrt(pcov[0][0])

#inizializzo una maschera in maniera tale da selezionare soltanto i
#den_abs diversi da zero, per avere un valore finito del chi2,
#che altrimenti divergerebbe
mask = den_abs != 0
oss = den_abs[mask]
ass = y[mask]

#test del chi2
chi2 = np.sum((ass-oss)**2 /oss)
ndf  = len(ld[mask])-len(p)
#stampo sul terminale il valore del chi2
print("\u03C7^2 / ndf = {:.4f}".format(chi2/ndf) )

#stampo il grafico del fit 
plt.plot(ld, den_abs, 'o', color='royalblue', label='punti del file')
plt.plot(ld, y, color='limegreen', label='curva del fit')
plt.xlabel(r'$\lambda$ (nm)')
plt.ylabel('densità fotoni')
plt.text(2e-6,0.8, r'T={:.0f} $\pm$ {:.0f} K'.format(p[0],error), fontsize=16)
plt.text(2e-6,0.7, r'$\chi$/ndf = {:.4f}'.format(chi2/ndf), fontsize=16)
plt.suptitle('fit dei punti forniti')
#plt.savefig('immagini/fit_funzione.jpeg')

plt.legend()
plt.show()


