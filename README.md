# progetto-esame

Progetto sviluppato per il corso di "Metodi computazionali per la fisica"
sullo scattering di Rayleigh per stelle diverse. All'interno della 
cartella 202302 si possono consultare il file con le istruzioni per lo
sviluppo del progetto ed un file contenente i dati relativi ad una
stella, oggetto della seconda parte del progetto sviluppato.

una seconda cartella "immagini" contiene tutte i grafici salvati in 
formato jpeg, queste saranno aggiunte alla presentazione che verrà
presentata in sede d'esame.

infine sono presenti i tre file seguenti:
 * funzioni.py
 * tramonti.py 
 * StellaX.py
 
funzioni.py
============
modulo all'interno del quale sono definite le funzioni che verranno 
richiamate all'interno degli altri due file.

tramonti.py
============
file contenente la prima parte del progetto in cui studiamo lo 
scattering di Rayleigh per 4 stelle:
 * Sole
 * Aldebaran
 * Vega
 * Spica
 
per selezionarle da terminale è necessario inserire il seguente comando:

	$ python3 tramonti.py --opzione

sostituendo ad opzione il nome della stella che si vuole studiare
(es: python3 tramonti.py --sole). 

Stellax.py
===========
in questo modulo è sviluppata l'ultima parte del progetto, ovvero 
lo studio del fit dei dati di una stella sconosciuta con la funzione 
densità di fotoni contenuta nel file funzioni.py, in modo da ricavare
la sua temperatura.
