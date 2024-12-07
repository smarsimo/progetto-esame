import sys, os
import numpy as np
import argparse
import matplotlib.pyplot as plt
import scipy
import matplotlib.ticker as tck

sys.path.append('funzioni.py')
import funzioni 

R_ter = 6.378e6  # m raggio della terra
T_s   = 5.75e3   # K temperatura del sole	
T_a   = 4e3      # K temperatura di Aldebaran
T_v   = 9.6e3    # K temperatura di Vega
T_sp  = 18e3     # K temperatura di Spica
n_ter = 1.00029  #   indice di rifrazione dell'aria
N_ter = 2.504e25 # mol/m^3 densità delle molecole presenti in atmosfera

#spessore della massa d'aria all'orizzonte
S_hor = np.sqrt((R_ter+8000)**2 - R_ter**2)

def parse_arguments():
	parser = argparse.ArgumentParser(description='simulazione diffusione di fotoni', usage='python3 tramonti.py --opzione')
	parser.add_argument('--sole',      action = 'store_true', help = "attraverso il metodo montecarlo, studia la distribuzione dei fotoni solari in funzione della lunghezza d'onda per tre diversi casi ed il flusso totale di fotoni in funzione della posizione del sole rispetto allo zenith")
	parser.add_argument('--aldebaran', action = 'store_true', help = "studio della distribuzione dei fotoni per Aldebaran")
	parser.add_argument('--vega',      action = 'store_true', help = "studio della distribuzione dei fotoni per Vega")
	parser.add_argument('--spica',     action = 'store_true', help = "studio della distribuzione dei fotoni per Spica")
	
	return parser.parse_args()

def scaled_den(l,T):
	"""
	funzione densità dei fotoni scalata in maniera tale che
	il massimo valore corrisponda ad 1
	"""
	return funzioni.den_fot(l,T)/max(funzioni.den_fot(l,T))

def scaled_den2(l, T, n, N, S):
	"""
	funzione densità dei fotoni scalata, quindi adatta al caso
	in cui si abbia assorbimento 
	"""
	return funzioni.abs_den(l, T, n, N, S)/max(funzioni.abs_den(l, T, n, N, S))

def tramonti():
	
	args = parse_arguments()
	
	if args.sole or args.aldebaran or args.vega or args.spica == True:

		N_estr=10000
		lmax = 2e-6
		lmin = 1e-7
		
		if args.sole == True:
			T = T_s
		elif args.aldebaran == True:
			T = T_a
		elif args.vega == True:
			T = T_v
		elif args.spica == True:
			T = T_sp
		
		lt  = np.linspace(lmin, lmax, N_estr)
		den = funzioni.den_fot(lt, T)
		
		#stampo la lunghezza d'onda che si ha in corrispondenza del picco
		m = den == max(funzioni.den_fot(lt, T))
		print("se non si ha assorbimento il picco di radiazione si ha in corrispondenza di:", lt[m])
		
		#grafico della densità dei fotoni che arrivano dalla stella
		plt.plot(     lt,den,color='royalblue'                                  )
		plt.suptitle( "densità dei fotoni in funzione della lunghezza d'onda (no assorbimento)")
		plt.xlabel(   r'$\lambda [\mu m]$'                                      )
		plt.ylabel(   'densità dei fotoni [$m^-3$]'                             )
		plt.show()
		
		#faccio un'estrazione della lunghezza d'onda nel dominio
		#di definizione, utilizzo il metodo hit or miss
		ld = np.random.uniform(lmin, lmax, N_estr)
		
		#estraggo anche la densità nell'intervallo [0,1]
		d_i = np.random.random(N_estr)
		
		#utilizzo un maschera per selezionare le lunghezze d'onda giuste
		mask1 = d_i <= scaled_den(ld, T)
		l_i = ld[mask1]
		
		#grafico della distribuzione dei fotoni che arrivano in caso di
		#non assorbimento
		plt.hist(l_i,bins=100,color='royalblue',ec='darkblue')
		plt.suptitle('distribuzione dei fotoni che arrivano in caso di non assorbimento')
		plt.xlabel(r'${\lambda}[\mu m]$')
		plt.ylabel(r'fotoni [$m^{-3}$]')		
		plt.show()			
		
		#utilizzo lo stesso metodo nel caso in cui si abbia 
		#assorbimento, in particolare nel caso in cui la stella
		#sia allo zenith
		mask2 = d_i <= scaled_den2(ld, T, n_ter, N_ter, 8000)
		l_i2  = ld[mask2]
		
		#stampo la lunghezza d'onda in cui si ha il picco di 
		
		#grafico usando l'array di lunghezze d'onda
		plt.plot(lt, funzioni.abs_den(lt, T, n_ter, N_ter, 8000),color='orange')
		plt.xlabel(r'$\lambda [\mu m]$')
		plt.ylabel(r'densità fotoni [$m^{-3}$]')
		plt.suptitle("densità dei fotoni in funzione della lunghezza d'onda (ZENITH)")
		plt.show()
		
		#metto in un istogramma i dati raccolti
		plt.hist(l_i2, bins=100,color='orange',ec='darkorange')
		plt.suptitle('distribuzione dei fotoni in caso di assorbimento (ZENITH)')
		plt.xlabel(r'${\lambda}[\mu m]$')
		plt.ylabel(r'fotoni [$m^{-3}$]')
		plt.show()
		
		#ancora una volta utilizzo una maschera, qui considero sempre
		#assorbimento, ma la stella si trova all'orizzonte
		mask3 = d_i <= scaled_den2(ld, T, n_ter, N_ter, S_hor)
		l_i3  = ld[mask3]
		
		#grafico della densità dei fotoni considerando la funzione 
		#densità nel caso in cui si abbia assorbimento e la stella si 
		#trovi all'orizzonte, usando l'array di lunghezze d'onda
		plt.plot(lt, funzioni.abs_den(lt, T, n_ter, N_ter, S_hor),color='turquoise')
		plt.xlabel(r'$\lambda [\mu m]$')
		plt.ylabel(r'densità dei fotoni [$m^{-3}$]')
		plt.suptitle("densità dei fotoni in funzione della lunghezza d'onda (ORIZZONTE)")
		plt.show()
		
		#grafico della distribuzione dei fotoni usando il metodo 
		#montecarlo
		plt.hist(l_i3, bins =100, color='turquoise', ec='lightseagreen')
		plt.suptitle('distribuzione dei fotoni in caso di assorbimento (ORIZZONTE)')
		plt.xlabel(r'${\lambda}[\mu m]$')
		plt.ylabel(r'fotoni [$m^{-3}$]')
		plt.show()
		
		#studio del flusso integrato di fotoni in funzione dell'angolo 
		#della posizione della stella rispetto allo zenith
		theta  = np.linspace(0,np.pi/2,100)
		m_s    = max(funzioni.abs_den(lt, T, n_ter, N_ter, 8000))
		S_th   = funzioni.th_airmass(R_ter, 8000, theta)
		fl_int = []
		
		#ciclo for per calcolare il flusso dei fotoni per ogni theta
		#li "appendo" nella lista fl_int per poi metterla in un grafico
		#con gli angoli
		for i in range(len(theta)):
			d_int    = np.random.random(N_estr)
			mask_int = d_int <= funzioni.abs_den(ld, T, n_ter, N_ter, S_th[i])/m_s
			l_int   = ld[mask_int]
			fl_int.append(len(l_int))
			
		f, ax = plt.subplots()
		ax.plot(theta/np.pi,fl_int,'-o',color='crimson')		
		ax.xaxis.set_major_formatter(tck.FormatStrFormatter(r'%g $\pi$'))
		ax.xaxis.set_major_locator(tck.MultipleLocator(base=0.1))
		plt.suptitle("flusso integrato di fotoni in funzione dell'angolo")
		plt.xlabel(r'$\theta$ [rad]')
		plt.ylabel("numero di fotoni $[m^{-3}]$")
		plt.show()
		
			
		
		
		


if __name__ == "__main__":
	tramonti()
