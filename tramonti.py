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

def parse_arguments():
	parser = argparse.ArgumentParser(description='simulazione diffusione di fotoni', usage='python3 tramonti.py --opzione')
	parser.add_argument('--solsc', action='store_true', help='produce un grafico della densità dei fotoni solari secondo teoria e altri tre grafici che simulano la distribuzione degli stessi in tre differenti casi')
	
	
	return parser.parse_args()

def scaled_den(l,T):
	"""
	funzione densità dei fotoni scalata in maniera tale che
	il massimo valore corrisponda ad 1
	"""
	return funzioni.den_fot(l,T)/max(funzioni.den_fot(l,T))

def tramonti():
	
	args = parse_arguments()
	
	if args.solsc == True:

		N_estr=10000
		lmax = 2e-6
		lmin = 1e-7
		
		lt=np.linspace(lmin,lmax,N_estr)
		den=funzioni.den_fot(lt,T_s)
		
		#grafico della densità dei fotoni che arrivano dal sole
		plt.plot(lt,den,color='royalblue')
		plt.suptitle("grafico della densità in funzione della lunghezza d'onda")
		plt.xlabel(r'$\lambda [\mu m]$')
		plt.ylabel('densità dei fotoni [$m^-3$]')
		plt.show()
		
		#faccio un'estrazione della lunghezza d'onda nel dominio
		#di definizione, utilizzo il metodo hit or miss
		ld=np.random.uniform(lmin,lmax,N_estr)
		
		#estraggo anche la densità nell'intervallo [0,1]
		d_i = np.random.random(N_estr)
		
		#utilizzo un maschera per selezionare le lunghezze d'onda giuste
		mask= d_i <= scaled_den(ld, T_s)
		l_i=ld[mask]

		#stampo le lunghezze d'onda estratte
		print("lunghezze d'onda estratte:", l_i)
		
		#grafico della distribuzione dei fotoni che arrivano in caso di
		#non assorbimento
		n,bins,_=plt.hist(l_i,bins=100,color='blue',ec='darkblue')
		plt.suptitle('distribuzione dei fotoni che arrivano in caso di non assorbimento')
		plt.xlabel(r'${\lambda}[\mu m]$')
		plt.show()	
		
		#creo una lista dove immagazzinare il numero di fotoni NON
		#diffusi nel caso in cui il cielo si trovasse allo zenith
		print(len(n))
		print(n)
		print(len(bins))
		print(bins)
		


if __name__ == "__main__":
	tramonti()
