import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize
import math

c=3e8       # m s^-1
h=6.626e-34 # J s
k=1.380e-23 # J K^-1

def rad_cn(l, T):
	"""
	funzione della radiazione del corpo nero: 
	rad_cn(l, T)=2*h*c^2/l^5 * 1/exp(h*c / l*k_b*T)-1 J m^-3 s^-1
	-----  PARAMETRI  -----
	l : lunghezza dell'onda irraggiata 
	T : temperatura del corpo nero
	----- RESTITUISCE -----
	la densità di energia irradiata da un corpo a temperatura T in 
	funzione della lunghezza d'onda
	"""
	sa=h*c
	so=l*k*T
	pt = (2*sa*c)/l**5
	st = 1/(np.exp(sa/so)-1)
	return pt*st

def den_fot(l, T):
	"""
	funzione densità di fotoni per lunghezza d'onda
	den_fot(l, T)=rad_cn/E_gamma 
	ove E_gamma è l'energia dei fotoni in funzione della lunghezza d'onda
	----- PARAMETRI -----
	l : lunghezza d'onda
	T : Temperatura del corpo nero
	"""
	E_gamma = h*c / l
	return rad_cn(l, T)*E_gamma

def beta_sc(l, n=1.00029, N=2.504e25):
	"""
	funzione che descrive la probabilità di interazione tra le onde
	e le particelle presenti nell'atmosfera
	beta_sc(l, n, N)=(8*pi^3 / 3*N*l^4)*(n^2-1)^2
	-----  PARAMETRI  -----
	l : lunghezza d'onda
	n : indice di rifrazione
	N : densità di molecole presenti nell'atmosfera
	----- RESTITUISCE -----
	il coefficiente di scattering di Rayleigh
	"""
	ter=(n**2 -1)**2
	so=3*N*l**4
	sa=8*np.pi**3
	return sa*ter/so


def N_obs(N_0, l, S):
	return N_0 * np.exp(-beta_sc(l)*S)


T_s  = 5.75e3 # K	
T_a  = 4e3    # K
T_sp = 18e3   # K
#consideriamo un range di lunghezze d'onda 
ld=np.linspace(0,2e-6,100)
plt.subplots(figsize=(9,10))
plt.plot(ld, den_fot(ld, T_s), color='purple'    )
plt.xlabel("${\lambda}$ [${\mu}m$]")
plt.ylabel('B [J$m^{-3}s^{-1}$]')
plt.suptitle("distribuzione dei fotoni solari in funzione della lunghezza d'onda")
plt.show()

distr=np.random.random(100)
obs_n=N_obs(distr, ld, 8000)
plt.plot(ld, N_obs(distr, ld, 8000))
plt.xlabel('$\lambda$ [$\mu$m]')
plt.ylabel('$N_{obs}$')
plt.suptitle("numero di particelle osservato in funzione del lunghezza d'onda")
plt.show()




