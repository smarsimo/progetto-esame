import sys, os
import numpy as np
import math
import decimal

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

def E_gamma(l):
	"""
	funzione che restituisce l'energia del fotone in funzione della
	lunghezza d'onda dello stesso
	"""
	return (h*c)/l

def den_fot(l, T):
	"""
	funzione densità di fotoni per lunghezza d'onda
	den_fot(l, T)=rad_cn/E_gamma 
	ove E_gamma è l'energia dei fotoni in funzione della lunghezza d'onda
	----- PARAMETRI -----
	l : lunghezza d'onda
	T : Temperatura del corpo nero
	"""
	return rad_cn(l, T)*E_gamma(l)

def beta_sc(l, n, N):
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
	ter=(n**2 -1)
	so=3*N*l**4
	sa=8*np.pi**3
	return sa * ter**2 /so


def abs_den(l, T, n, N, S):
	"""
	funzione che restituisce il numero di fotoni nel caso in cui 
	si abbia assorbimento 
	abs_den=den_fot(l,T)*exp(-beta_sc(l,n,N)*S)
	-----  PARAMETRI  -----
	l : lunghezza d'onda
	T : temperatura della stella
	n : indice di rifrazione
	N : densità di molecole
	S : spessore della massa d'aria
	----- RESTITUISCE -----
	densità di fotoni in funzione dello spessore della massa
	d'aria
	"""
	return den_fot(l,T) * np.exp(-beta_sc(l,n,N) * S)





