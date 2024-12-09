import sys, os
import numpy as np
import argparse
import matplotlib.pyplot as plt
from scipy import optimize
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
		
		#faccio un'estrazione della lunghezza d'onda nel dominio
		#di definizione, utilizzo il metodo hit or miss
		ld = np.random.uniform(lmin, lmax, N_estr)
		
		#estraggo anche la densità nell'intervallo [0,1]
		d_i = np.random.random(N_estr)
		
		#utilizzo un maschera per selezionare le lunghezze d'onda giuste
		mask1 = d_i <= scaled_den(ld, T)
		l_i = ld[mask1]
		
		#grafico della densità dei fotoni che arrivano dalla stella
		fig, (ax1, ax2) = plt.subplots(2, sharex=True)
		fig.suptitle( "densità e distribuzione dei fotoni in funzione della lunghezza d'onda (no assorbimento)")
		ax1.plot(lt,den,color='royalblue'           )
		ax1.set(ylabel='densità dei fotoni [$m^-3$]'                             )
		
		#grafico della distribuzione dei fotoni che arrivano in caso di
		#non assorbimento
		ax2.hist(l_i,bins=100,color='royalblue',ec='darkblue')
		ax2.set(xlabel=r'${\lambda}[\mu m]$')
		ax2.set(ylabel=r'fotoni [$m^{-3}$]')		
		plt.show()			
		
		#utilizzo lo stesso metodo nel caso in cui si abbia 
		#assorbimento, in particolare nel caso in cui la stella
		#sia allo zenith
		mask2 = d_i <= scaled_den2(ld, T, n_ter, N_ter, 8000)
		l_i2  = ld[mask2]
		
		#stampo la lunghezza d'onda in cui si ha il picco di 
		abd = funzioni.abs_den(lt, T, n_ter, N_ter, 8000)
		m2  = abd == max(funzioni.abs_den(lt, T, n_ter, N_ter, 8000))
		print("nel caso si trovi allo zenith, il picco di radiazione si ha in corrispondenza di: ",lt[m2])
		
		#grafico usando l'array di lunghezze d'onda
		fig, (ax3, ax4) = plt.subplots(2,sharex=True)
		ax3.plot(lt, abd,color='orange')
		ax3.set(ylabel=r'densità fotoni [$m^{-3}$]')
		fig.suptitle("densità e distribuzione dei fotoni in funzione della lunghezza d'onda (ZENITH)")
		
		#metto in un istogramma i dati raccolti
		ax4.hist(l_i2, bins=100,color='orange',ec='darkorange')
		ax4.set(xlabel=r'${\lambda}[\mu m]$')
		ax4.set(ylabel=r'fotoni [$m^{-3}$]')
		plt.show()
		
		#ancora una volta utilizzo una maschera, qui considero sempre
		#assorbimento, ma la stella si trova all'orizzonte
		mask3 = d_i <= scaled_den2(ld, T, n_ter, N_ter, S_hor)
		l_i3  = ld[mask3]
		
		#stampo anche in questo caso la lunghezza d'onda dove si 
		#ha il picco
		abd2 = funzioni.abs_den(lt, T, n_ter, N_ter, S_hor)
		m3   = abd2 == max(funzioni.abs_den(lt, T, n_ter, N_ter, S_hor))
		print("nel caso in cui il sole sia all'orizzonte, il picco di radiazione si ha in corrispondenza di:", lt[m3])
		
		#grafico della densità dei fotoni considerando la funzione 
		#densità nel caso in cui si abbia assorbimento e la stella si 
		#trovi all'orizzonte, usando l'array di lunghezze d'onda
		fig, (ax5, ax6) = plt.subplots(2,sharex=True)
		ax5.plot(lt, abd2,color='turquoise')
		ax5.set(ylabel=r'densità dei fotoni [$m^{-3}$]')
		fig.suptitle("densità e distribuzione dei fotoni in funzione della lunghezza d'onda (ORIZZONTE)")
		
		#grafico della distribuzione dei fotoni usando il metodo 
		#montecarlo
		ax6.hist(l_i3, bins =100, color='turquoise', ec='lightseagreen')
		ax6.set(xlabel=r'${\lambda}[\mu m]$')
		ax6.set(ylabel=r'fotoni [$m^{-3}$]')
		plt.show()
		
		#studio del flusso integrato di fotoni in funzione dell'angolo 
		#della posizione della stella rispetto allo zenith
		theta  = np.linspace(0.01,np.pi/2,80)
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
			
		#print("per questa simulazione, tra lo zenith e l'orizzonte si ha una differenza di", fl_int[0]-fl_int[99], 'fotoni')
		f, ax = plt.subplots()
		ax.plot(theta/np.pi,fl_int,'-o',color='crimson')		
		ax.xaxis.set_major_formatter(tck.FormatStrFormatter(r'%g $\pi$'))
		ax.xaxis.set_major_locator(tck.MultipleLocator(base=0.1))
		plt.suptitle("flusso integrato di fotoni in funzione dell'angolo")
		plt.xlabel(r'$\theta$ [rad]')
		plt.ylabel("numero di fotoni $[m^{-3}]$")
		plt.show()
		
		#provop a fare il fit con una funzione per interpretare 
		#il modo in cui decresce il flusso di fotoni in 
		#funzione dell'angolo theta
		def fit(x, A, B, C):
			"""
			funzione per il fit con i dati dei fotoni tilevati
			in funzione dell'angolo che individua la posizione 
			della stella rispetto allo Zenith
			"""
			return A*np.log(B*x + C)

		pstart = np.array([1,1,0])
		p, pcov = optimize.curve_fit(fit, theta, fl_int, p0=[pstart])
		print("i valori ricavati dal fit per le costanti sono: A =", p[0],", B =", p[1]," e C = ", p[2])
		y = fit(theta, p[0], p[1], p[2])
		plt.plot(theta,fl_int, 'o', color='crimson')
		plt.plot(theta,y, color='slateblue')
		plt.suptitle('fit dei dati con una funzione logaritmica')
		plt.xlabel(r'$\theta$ [rad]')
		plt.ylabel('fotoni $m^{-3}$')
		plt.show()
		
		#test del chi quadro
		chi2 = np.sum((y-fl_int)**2 /fl_int)
		ndf  = len(theta)-len(p)
		print("\u03C7^2 / ndf = ",chi2/ndf )
		


if __name__ == "__main__":
	tramonti()
