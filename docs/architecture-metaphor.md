# RAPPRESENTAZIONE VISIVA DEL MIO PROGETTO DEVOPS


# io parto da una struttura che è il mio studio (immagina 12 m2 di stanza)
# È COME SE FOSSE IL MIO PC FISICO

###

# su questo pc fisico installo VMWARE. 
# VMWARE HA UN HYPERVISOR CHE MI PERMETTE DI CREARE MACCHINE VIRTUALI

# il software che gira sul fisico è:

#	- VMware 
#	- Hypervisor 

# il PC fisico esegue un hypervisor (VMware) che permette di creare macchine virtuali isolate, che si comportano come sistemi indipendenti.

###

# per il momento sono ancora sul mio pc fisico. non sto virtualizzando niente

###

# creo la mia VM server-lab-01
# è come se progettassi di aggiungere una stanza al mio studio
# è una stanza virtuale, non la costruisco veramente (è appunto virtuale)

###

# creo la VM, metto LINUX SERVER ed è come se ora oltre al mio studio avessi una stanza in più (virtuale)
# quindi ora la mia casa diventa studio + stanza virtuale

	## - Il mio PC fisico = studio
	## - La VM = nuova stanza (virtuale) dentro casa

# Non è un altro edificio: usa le stesse risorse (CPU, RAM, disco) ma è isolata come se fosse separata

###

# Traduzione tecnica
# - Studio = PC fisico (hw reale)
# - Stanza virtuale (VM) = server-lab-01 -> ambiente isolato dove gira LINUX SERVER
# - Casa = Studio + VM

###

# dentro la VM ho messo LINUX SERVER
# è un sistema operativo su cui girano programmi che servono un CLIENT
# è un sistema operativo che permette ai servizi di girare e rispondere ai CLIENT
# questi servizi / programmi sono ad esempio NGINX e FLASK 

###

# Il CLIENT è QUALSIASI cosa che fa una richiesta al tuo SERVER (VM server-lab-01) ad esempio:

	# - curl
	# - browser
	# - un altro SERVER: un frontend chiama una API oppure un microservizio chiama un altro servizio
	# - un APP mobile sul cel che chiama un BACKEND (FLASK API)

### CLIENT = programma che genera e invia una richiesta (in genere e nel mio caso HTTP) a un SERVER ###

# io sono l’umano che usa questi CLIENT 

###

# LOCALHOST = l’indirizzo con cui un CLIENT parla a servizi sulla stessa macchina

#####	NGINX 	####


# la prima cosa che ho installato è NGINX

# NGINX è un WEB SERVER e un REVERSE PROXY che riceve richieste dai CLIENT e le inoltra ai servizi (interni o esterni - e per esterni 
# si intende altre VM / PROGRAMMI / SERVIZI / BACKEND nella mia LAN o sull'internet globale - ), restituendo poi la risposta al CLIENT'

# NGINX ha un file di configurazione che si trova in '/etc/nginx/nginx.conf' configurato per ascoltare e ricevere 
# richieste HTTP sulla porta 80. 

# test NGINX: curl http://127.0.0.1


##

# NGINX è un carrello (intelligente) all’ingresso della mia stanza virtuale (VM) che riceve le richieste dei CLIENT, decide come gestirle 
# (rispondere direttamente o inoltrarle al backend) e restituisce la risposta al CLIENT
# Nel mio caso NGINX inoltra le richieste a un servizio interno alla VM (FLASK) e restituisce la risposta

##

# poi abbiamo installato FLASK 

# FLASK è una CASSETTA DEGLI ATTREZZI per costruire BACKEND web (API HTTP) in Python

# FLASK è un micro web framework in Python che permette di creare applicazioni web e API HTTP, gestendo richieste e generando 
# risposte tramite codice Python

# FLASK è il componente che:
  #	- ascolta su una porta (5000)
  #	- riceve richieste HTTP
  #	- le associa a funzioni Python (routing)
  #	- esegue la logica
  #	- restituisce una risposta (stringa o JSON)



###

# poi abbiamo creato un'API

# Una API (Application Programming Interface) è un insieme di regole, endpoint e formati che permette a un software (client) di comunicare 
# con un altro software (server) per richiedere ed ottenere dati o operazioni.# # #  # #  


# METAFORA: API è il “modo ufficiale” con cui puoi parlare con un servizio. Un’API è il contratto di comunicazione tra CLIENT e SERVE# R### Un ENDPOINT è un indirizzo specifico della tua API dove un CLIENT può f# are una richiesta.

# È una combinazione di:

 # - URL → /users

 # - metodo HTTP → GET, POST, ecc.


####	#####	#####	#####

# SYSTEMD = primo processo (PID 1) che parte all’avvio e gestisce tutti gli altri servizi.

###

# Prima di SYSTEMD, il mio flusso era manuale:

 # - Entravo nella VM
 # 
 # - Attivavi l’ambiente: 
 
 source /var/www/devopsapp/backend/venv/bin/activate

# Avviavo FLASK: 

 python app.py

# Tradotto: ogni volta dovevo “accendere a mano” il backend

# Ed è proprio il problema che SYSTEMD risolve

###

# Configurazione essenziale che ho fatto:

# Creazione service file
sudo nano /etc/systemd/system/devopsapp.service
# Contenuto (logica)
# definisco utente
# definisco path progetto
# faccio partire FLASK con Python del venv

#struttura:

# file inizio


[Unit]
Description=DevOps Flask App
After=network.target

[Service]
User=dprandi
WorkingDirectory=/var/www/devopsapp/backend
ExecStart=/var/www/devopsapp/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
 
# file fine 


# Ricarichi systemd
sudo systemctl daemon-reexec
sudo systemctl daemon-reload


# Avvio
sudo systemctl start devopsapp

# Abilitazione al boot
sudo systemctl enable devopsapp

# Tradotto nella tua metafora

# systemd = il “gestore automatico” della macchina
# invece di avviare Flask a mano, gli dici:
# “quando si accende tutto, fallo partire tu”



######	######		GUNICORN	######	######

# Gunicorn è un application server WSGI che esegue applicazioni Python (es. Flask) in modo stabile e scalabile per ambienti di 
# produzione. 

# Flask = il tuo codice (app)

# Gunicorn = il motore che lo esegue in modo serio

# Gestisce:

	# più richieste insieme (worker)
	# stabilità
	# processi


# METAFORA
	# Flask (dev server) = un impiegato da solo alla scrivania

	# Gunicorn = un ufficio con più impiegati coordinati

	# NGINX = il portinaio che smista le persone


# Differenza chiave Flask vs Gunicorn

	# Flask (quando fai python app.py)
		
		# server di sviluppo
		
		# 1 richiesta alla volta

		# non stabile sotto carico
		
		# non sicuro per produzione

		# serve per sviluppare

	# Gunicorn

		# più worker (processi)
		
		# gestisce più richieste contemporaneamente

		# stabile

		# usato in produzione

		# serve per far girare davvero l’app

# Flusso corretto in produzione
	
	# Client → NGINX → Gunicorn → Flask (app)

# Frase forte

	# Flask definisce l’app, Gunicorn la esegue in modo scalabile, NGINX la espone al mondo

# Errore classico (importantissimo)

	# NON usare mai python app.py in produzione

# Nel mio lab (step successivo naturale) al posto di:

python app.py

# userò:

gunicorn -w 4 -b 127.0.0.1:5000 app:app



######	######		DOCKER	######	######


# Docker è una piattaforma che permette di creare, distribuire ed eseguire applicazioni in contenitori (container) isolati e portabili.


# Cosa fa in pratica
	
	# prende la tua applicazione + dipendenze  
	
	# le “impacchetta” in un container  
	
	# la fa girare uguale ovunque (VM, server, cloud)


# Concetto chiave

	# container = ambiente isolato leggero dove gira la tua app



# Metafora
	
	#  Senza Docker:
	
	#  ogni server è diverso → “funziona solo sul mio PC”
	 
	#  Con Docker:
	
	#  è come una scatola standardizzata  
	
	#  dentro c’è tutto (app + librerie)  
	
	#  la porti ovunque e funziona uguale


# Frase chiave

# Docker elimina il problema “sul mio computer funziona” rendendo l’app portabile e replicabile


# Collegamento al lab

# Prima:
	
	# VM → installi Python → venv → Flask → config manuale

	# Con Docker:
		
		# Container → dentro hai già tutto pronto → lo avvii e basta
		
		

source /var/www/devopsapp/backend/venv/bin/activate

# TEST GUNICORN

gunicorn -w 4 -b 127.0.0.1:5000 app:app

# ERRORE - FLASK GIA' IN ASCOLTO SU PORTA 5000

sudo ss -tulnp | grep 5000

sudo systemctl stop devopsapp

# riprovo

gunicorn -w 4 -b 127.0.0.1:5000 app:app 

# e funziona

# ora lo automatizzo con demone systemd 

sudo nano /etc/systemd/system/devopsapp.service

# file INIZIO

[Unit]
Description=DevOps Flask API
After=network.target

[Service]
User=dprandi
WorkingDirectory=/var/www/devopsapp/backend

#FLASK
#ExecStart=/var/www/devopsapp/backend/venv/bin/python app.py

#GUNICORN
ExecStart=/var/www/devopsapp/backend/venv/bin/gunicorn --chdir /var/www/devopsapp/backend --workers 4 --bind 127.0.0.1:>
Restart=always

[Install]
WantedBy=multi-user.target

#file FINE 


sudo systemctl daemon-reload

sudo systemctl restart devopsapp

sudo systemctl status devopsapp

curl http://localhost


systemd → Gunicorn → Flask
           ↑
        NGINX
           ↑
        Client
		
		

