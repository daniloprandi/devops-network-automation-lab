RAPPRESENTAZIONE VISIVA DEL MIO PROGETTO DEVOPS

io parto da una struttura che è il mio studio (immagina 12 m2 di stanza)

E' come se fosse il mio PC FISICO

Su questo PC FISICO installo VMWARE. 

VMWARE ha un HYPERVISOR che mi permette di creare MACCHINE VIRTUALI

Il software che gira sul PC FISICO è:

- VMware
- Hypervisor

il PC FISICO esegue un HYPERVISOR (VMWARE) che permette di creare macchine virtuali isolate, che si comportano come SISTEMI indipendenti.

Adesso sono ancora sul mio PC FISICO. 

Non sto virtualizzando niente

Adesso creo la mia VM 'server-lab-01'

E' come se progettassi di aggiungere una stanza al mio studio

E' una stanza virtuale, non la costruisco veramente (è, appunto, virtuale)

Creo la VM ed è come se ora, oltre al mio studio, avessi una stanza in + (virtuale)

Quindi ora la mia casa diventa studio + stanza virtuale

## - Il mio PC FISICO = studio

## - La VM che creo con il mio PC FISICO = nuova stanza (virtuale) dentro casa

Non è un altro edificio: usa le stesse risorse (CPU, RAM, disco) ma è isolata ed è come se fosse separata

Traduzione tecnica

- Studio = PC fisico (hw reale)
- Stanza virtuale (VM) = server-lab-01 -> ambiente isolato dove gira LINUX SERVER
- Casa = Studio + VM

Dentro la VM ho messo LINUX SERVER

LINUX SERVER è un sistema operativo su cui girano programmi che servono un CLIENT

LINUX SERVER permette ai servizi di girare e rispondere ai CLIENT (esempi di CLIENT: curl, browser)

questi servizi / programmi sono ad esempio NGINX e FLASK

CLIENT = programma che genera e invia una richiesta (in genere e nel mio caso HTTP) a un SERVER 

Io sono l’umano che usa questi CLIENT

Il CLIENT è qualsiasi cosa che fa una richiesta al SERVER 'server-lab-01', ad esempio:

# curl

# browser

# un altro SERVER: un frontend chiama una API oppure un microservizio chiama un altro servizio

# un APP mobile sul cel che chiama un BACKEND (FLASK API)

LOCALHOST = nome che identifica la MACCHINA stessa; viene risolto nell’indirizzo di loopback (127.0.0.1 in IPv4, ::1 in IPv6) 

LOCALHOST indica che la comunicazione resta interna al sistema, senza uscire sulla rete. 

LOCALHOST usa l’interfaccia di loopback, che su Linux si chiama 'lo'



################################################

###### 			NGINX		 ###########################

################################################


NGINX (primo strumento che ho installato) = è un WEB SERVER e un REVERSE PROXY che riceve le richieste dai CLIENT, le gestisce e le inoltra al BACKEND, proteggendolo (il BACKEND) e migliorando le prestazioni. 

NGINX nasconde PORTE, STRUTTURA INTERNA e SERVIZI del BACKEND

NGINX filtra, instrada e protegge

NGINX riceve le richieste dei CLIENT e le inoltra ai servizi (interni o esterni: esterni = altre VM / PROGRAMMI / SERVIZI / BACKEND nella mia LAN o sull'internet globale - ), restituendo poi la risposta al CLIENT'

NGINX ha un file di configurazione che si trova in '/etc/nginx/nginx.conf' configurato per ascoltare e ricevere richieste HTTP 
sulla porta 80.

*** test NGINX: curl http://127.0.0.1 ***

NGINX è un CARRELLO (intelligente) all’interno della mia VM (e successivamente sarà spostato dentro DOCKER) che riceve le richieste dei CLIENT, decide come gestirle (rispondere direttamente o inoltrarle al backend) e restituisce la risposta al CLIENT


poi abbiamo installato FLASK


################################################

###### 			FLASK		 ###########################

################################################


FLASK è una CASSETTA DEGLI ATTREZZI per costruire BACKEND web (API che usano HTTP) in Python 

FLASK è una CASSETTA DEGLI ATTREZZI con cui costruisco un COMODINO (l’API) e definisco come deve funzionare

FLASK è un MICRO WEB FRAMEWORK in Python che permette di creare applicazioni web e API (che usano HTTP), gestendo richieste e generando
risposte tramite codice Python

FLASK è il componente che:

- ascolta su una porta (5000)

- riceve richieste HTTP

- le associa a funzioni Python (routing)

- esegue la logica

- restituisce una risposta (stringa o JSON)

poi abbiamo creato un'API



################################################

###### 			API		 #############################

################################################



API (Application Programming Interface) = insieme di regole, ENDPOINT e formati (JSON, YAML, XML) che permette a un software (CLIENT) di comunicare con un altro software (SERVER) per richiedere ed ottenere dati o operazioni

Un’API espone ENDPOINT accessibili tramite HTTP, permettendo ai CLIENT di inviare richieste e ricevere risposte strutturate, tipicamente in formato JSON.

Un’API è il COMODINO che espone dei CASSETTI (ENDPOINT) attraverso cui il CLIENT può chiedere qualcosa al sistema

API è il "modo ufficiale" con cui puoi parlare con un servizio. 

API è il contratto di comunicazione tra CLIENT e SERVER

ENDPOINT = indirizzo specifico della tua API dove un CLIENT può fare una richiesta.

ENDPOINT = punto di accesso specifico di un’API, identificato da un URL e un metodo HTTP, attraverso cui un CLIENT può richiedere una determinata operazione.

ENDPOINT = punto di accesso a una funzionalità dell’API, identificato da un URL e un metodo HTTP.

È una combinazione di:

- URL → /users

- metodo HTTP → GET, POST, ecc. 




################################################

###### 			LINUX SERVER		 ###################

################################################


SYSTEMD = primo processo (PID 1) che parte all’avvio e gestisce tutti gli altri servizi

Prima di SYSTEMD, il mio flusso era manuale:

- Entravo nella VM

- Attivavo l’ambiente: 'source /var/www/devopsapp/backend/venv/bin/activate'

- Avviavo FLASK: 'python app.py'

***		Tradotto: ogni volta dovevo “accendere a mano” il backend		***

E' proprio il problema che SYSTEMD risolve

Configurazione essenziale che ho fatto:

- Creazione service file 'sudo nano /etc/systemd/system/devopsapp.service'

Contenuto (logica)

- definisco utente

- definisco path progetto

- faccio partire FLASK con Python del venv

Struttura del file 'devopsapp.service':

***		INIZIO		***

[Unit] Description=DevOps Flask App After=network.target

[Service] User=dprandi WorkingDirectory=/var/www/devopsapp/backend ExecStart=/var/www/devopsapp/backend/venv/bin/python app.py Restart=always

[Install] WantedBy=multi-user.target

***		FINE		***

RICARICO processo 'systemd' (PID 1)con comando 'sudo systemctl daemon-reexec sudo systemctl daemon-reload'

Lo AVVIO 'sudo systemctl start devopsapp'

Lo abilito al BOOT 'sudo systemctl enable devopsapp'

***		Tradotto		*** 

systemd = il “gestore automatico” della macchina

invece di avviare Flask a mano, gli dico: 'quando si accende tutto, fallo partire tu'



################################################

###### 			GUNICORN		 ###################

################################################



GUNICORN = Application Server WSGI che esegue applicazioni Python (es. FLASK) in modo stabile e scalabile per ambienti di produzione.

FLASK = il mio codice (app)

GUNICORN = il MOTORE che esegue il codice FLASK in modo serio

GUNICORN gestisce:

# più richieste / processi insieme (worker)

# stabilità

# processi

METAFORA

# Flask (dev server) = un impiegato da solo alla scrivania

# Gunicorn = un ufficio con più impiegati coordinati

# NGINX = il portinaio che smista le persone

***		Differenza chiave FLASK vs GUNICORN		***

# FLASK (quando fai python app.py)
	
	# server di sviluppo
	
	# 1 richiesta alla volta

	# non stabile sotto carico
	
	# non sicuro per produzione

	# serve per sviluppare

# GUNICORN

	# più worker (processi)
	
	# gestisce più richieste contemporaneamente

	# stabile

	# usato in produzione

	# serve per far girare davvero l’app
	
	
Flusso corretto in produzione -> 'Client 	→ 	NGINX 	→ 	Gunicorn 	→ 	Flask (app)'

FRASE FORTE

# FLASK definisce l’app

# GUNICORN la esegue in modo scalabile

# NGINX la espone al mondo

ERRORE CLASSICO (IMPORTANTISSIMO): NON usare mai 'python app.py' in produzione

Nel mio lab (step successivo naturale) al posto di:

python app.py

userò:

gunicorn -w 4 -b 127.0.0.1:5000 app:app


################################################

###### 			DOCKER		 #########################

################################################



DOCKER = piattaforma che permette di creare, distribuire ed eseguire applicazioni in contenitori (CONTAINER) isolati e portabili.

Cosa fa in pratica

# prende la tua applicazione + dipendenze  

# le 'impacchetta' in un CONTAINER  

# la fa girare uguale ovunque (VM, server, cloud)


CONTAINER = ambiente isolato leggero dove gira la mia app

Metafora

#  Senza DOCKER -> ogni SERVER è diverso → 'funziona solo sul mio PC'
 
#  Con DOCKER -> è come una scatola standardizzata  

#  dentro c’è tutto (app + librerie)  

#  la porti ovunque e funziona uguale

Frase chiave

DOCKER elimina il problema 'sul mio computer funziona' rendendo l’app portabile e replicabile

Collegamento al lab

Prima:

# VM → installi Python → venv → Flask → config manuale

# Con DOCKER:
	
	# Container → dentro hai già tutto pronto → lo avvii e basta
	
	
	
################################################

###### 			UNIX SOCKET		 #####################

################################################



COSA HO FATTO FINO A ORA?

# sto comunicando via rete (TCP/IP) anche se sono sulla stessa macchina (VM)

Il prossimo step: UNIX SOCKET

Adesso cambiamo COME comunicano i processi:

Prima: 

'Nginx 		-> 		HTTP 		-> 		127.0.0.1:5000 		-> 		Gunicorn 		-> 		Nginx bussa a una porta (5000)'

Dopo:		

'Nginx 		-> 		FILE (/run/devopsapp.sock) 		-> 	Gunicorn 		-> 		Nginx lascia richieste dentro una cassetta fisica (file .sock)

-> 	 Gunicorn passa e le legge'


cambia tutto:

# non passi più dalla rete

# passi dal filesystem

# è più veloce

# è più 'da sistemista vero'

# niente rete, solo comunicazione interna alla macchina

modifico GUNICORN

sudo nano /etc/systemd/system/devopsapp.service

ExecStart=/var/www/devopsapp/backend/venv/bin/gunicorn --chdir /var/www/devopsapp/backend --workers 4 --bind 127.0.0.1:5000 app:app

#file corretto

[Unit] Description=DevOps Flask API After=network.target

[Service] User=dprandi Group=www-data

WorkingDirectory=/var/www/devopsapp/backend

RuntimeDirectory=devopsapp

#FLASK #ExecStart=/var/www/devopsapp/backend/venv/bin/python app.py

#GUNICORN

ExecStart=/var/www/devopsapp/backend/venv/bin/gunicorn --chdir /var/www/devopsapp/backend --workers 4 --bind 127.0.0.1:5000 app:app
UNIX SOCKET
ExecStart=/var/www/devopsapp/backend/venv/bin/gunicorn --workers 3 --bind unix:/run/devopsapp/devopsapp.sock app:app

Restart=always

PERMESSI SOCKET
User=www-data
Group=www-data

#OPPURE

[Install] WantedBy=multi-user.target

PERMESSI SOCKET
User=www-data Group=www-data

oppure (uso questi)
User=dprandi Group=www-data

Nginx gira come www-data, quindi deve poter leggere il socket: 'sudo systemctl daemon-reexec sudo systemctl daemon-reload sudo systemctl' 

restart devopsapp

CONTROLLO
ls /run/

e devo vedere
devopsapp.sock

modifico NGINX /etc/nginx/sites-available/devopsapp

#server {

listen 80;
server_name localhost;
location / {
proxy_pass http://127.0.0.1:5000;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
}
#}

nuovo file (unix socket / gunicorn)
server { listen 80;

location / {
    proxy_pass http://unix:/run/devopsapp/devopsapp.sock;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
}

ora il flusso è questo
Client → Nginx → UNIX SOCKET → Gunicorn → Flask



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!			QUI DEVO VEDERE BENE 

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




prendiamo questa strada (aziendale)

# Docker backend

# Nginx host

poi deploy style production

cd $DEVOPSAPP_HOME/backend

crea file 'requirements.txt' (se non ce l’hai)

pip freeze > requirements.txt

crea Dockerfile

nano Dockerfile

dentro metto



*** INIZIO FILE ***


FROM python:3.11-slim
# usa immagine base Python leggera (OS + Python già pronto)

WORKDIR /app
# crea/imposta cartella di lavoro interna al container

COPY . .
# copia tutti i file del progetto locale dentro /app del container

RUN pip install --no-cache-dir -r requirements.txt
# installa dipendenze Python (Flask, psycopg2, gunicorn...)

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
# avvia Gunicorn:
# -w 3 = 3 worker/processi
# -b = ascolta su porta 5000 su tutte le interfacce
# app:app = file app.py -> oggetto Flask chiamato app


*** FINE FILE ***


# installo DOCKER

sudo apt update && sudo apt install docker.io -y

# avvio Docker

sudo systemctl start docker

# Abilito Docker all’avvio

sudo systemctl enable docker

docker --version

###	STEP IMPORTANTISSIMO (permessi): se provi a usare docker così, ti darà errore. Devi fare:

sudo usermod -aG docker $USER

# riavvio VM

sudo reboot

# Test finale: Se NON chiede sudo → sei a posto

docker ps

# Traduzione semplice: Docker = nuovo “motore” nella tua VM. lo hai appena installato. ora puoi creare CONTAINER

# poi vado in 'cd $DEVOPSAPP_HOME/backend' e faccio

docker build -t devopsapp-backend .

# quel . = usa QUESTA cartella

# ora avvio il Container


--

# avvio il container backend in background
docker run -d \

# -d = detached mode → gira in background

-p 127.0.0.1:5000:5000 \

# mappa porta host → container

# host VM: 127.0.0.1:5000

# container: porta 5000 (Gunicorn/Flask)

--name devopsapp \

# assegna nome al container

devopsapp-backend

# nome dell'immagine Docker creata con docker build

--

# test

docker ps

curl http://127.0.0.1:5000

# docker run (errore, no params)

# ora collego nginx al container Docker

sudo nano /etc/nginx/sites-available/devopsapp

# aggiorno file

server { listen 80;

location / {
    proxy_pass http://127.0.0.1:5000;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
}


# guardo se funziona

curl http://127.0.0.1


# ricevo err 502 (backend non raggiungibile)

docker ps

# ho lista vuota: container non attivo

# rimettiamo SU il BACKEND

docker rm -f devopsapp 2>/dev/null

# lo avviamo

docker run -d
-p 127.0.0.1:5000:5000
--restart always
--name devopsapp
devopsapp-backend

# tutto ok. vedo il container con

docker ps

adesso il comando funziona (nginx risponde)
curl http://127.0.0.1

FLUSSO: 'Client 	→ 	Nginx 	→ 	Docker 	→ 	Gunicorn 	→ 	Flask





!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!			RIPRENDERE DA QUI 			!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!







########## DOCKER COMPOSE ################  !!! RIP DA QUI !!!

# PRIMA: accendi ogni macchina a mano

# Con compose: hai un quadro elettrico centrale

METAFORA (perfetta per capirlo)

systemd -> è il quadro elettrico della casa: accende le luci, gestisce gli impianti, tutto interno alla casa (OS)

docker-compose -> è il responsabile dei container/scatole, decide quali scatole usare, le accende tutte insieme, le collega tra loro

systemd gestisce i processi dell’host, docker-compose orchestra i container applicativi
cd $DEVOPS_APP/backend

# creo file COMPOSE

nano docker-compose.yml

version: "3.9"

services: backend: build: . container_name: devopsapp ports: - "127.0.0.1:5000:5000" restart: always



METAFORA: Cosa ho fatto? Ho scritto: “questo è il mio servizio backend”

build → usa Dockerfile

porta → 5000

restart → automatico

FERMO VECCHIO Container

docker rm -f devopsapp

avvio con compose

docker compose up -d

faccio docker ps e devo vedere il container

docker ps

comandi IMPORTANTISSIMO

docker compose down

docker compose up -d

rebuild (quando cambio codice)

docker compose up -d --build

ora il flusso è

RETE DOCKER INTERNA = SALTO VERO

passo da
nginx → 127.0.0.1:5000

a
nginx → backend

senza localhost, senza porte esposte, comunicazione tra servizi
“I container comunicano tramite network Docker usando il nome del servizio come hostname”
#FLUSSO ATTUALE

Client → Nginx (container) → backend (container) → Gunicorn → Flask

cd $DEVOPSAPP_HOME

creo cartella nginx
mkdir nginx cd nginx nano default.conf

server { listen 80;

location / {
    proxy_pass http://backend:5000;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
}

# qui succede la magia:

# backend:5000: NON è IP → è nome servizio Docker

# modifico DOCKER COMPOSE

cd /var/www/devopsapp/backend
nano docker-compose.yml

# COSA CAMBIA: expose → visibile SOLO dentro Docker | niente più 127.0.0.1 | nginx parla con backend

# fermo tutto

docker-compose down

# avvio nuova architettura

docker-compose up -d --build

# verifico

docker ps

# Devo vedere:

devopsapp-backend
devopsapp-nginx

# errore porta 80 occupata

sudo systemctl stop nginx

# poi rilancio docker

docker-compose down
docker-compose up -d --build

# test

curl http://127.0.0.1

# OK

# LEZIONE DEVOPS: quando containerizzi un servizio devi decidere chi “possiede” la porta

# ora il flusso è

Client → Nginx (container) → backend (container)

### 28/04/2026

##### POSTGRES SQL #####

- aggiungiamo il database in Docker
- lo teniamo isolato (come backend)
- lo rendiamo raggiungibile come db:5432

# Config (docker-compose.yml)

cd /var/www/devopsapp/backend

db:  # definisco servizio database (nome = hostname "db" nella rete Docker)

  image: postgres:15  # uso immagine ufficiale PostgreSQL versione 15

  environment:  # variabili per inizializzare il DB
    POSTGRES_DB: devopsdb        # nome database creato automaticamente
    POSTGRES_USER: devopsuser    # utente DB
    POSTGRES_PASSWORD: devopspassword  # password DB

  volumes:
    - postgres_data:/var/lib/postgresql/data  # persistenza dati (non si perdono al restart)

  expose:
    - "5432"  # porta DB visibile SOLO nella rete Docker (non verso esterno)

volumes:
  postgres_data:  # volume Docker usato per salvare i dati del database

Perché? crei il DB dentro Docker (non esposto, solo interno)

## AVVIO tutto

ricostruiamo i container

avviamo anche il DB

allineiamo l’ambiente



docker-compose down
docker-compose up -d --build

Perché? Docker prende la nuova config e crea il container DB

entriamo in PostgreSQL

verifichiamo che sia attivo

testiamo accesso

Comando

docker exec -it backend_db_1 psql -U devopsuser -d devopsdb

Perché? controlli che il DB sia realmente funzionante

creo tabella

Cosa facciamo

creiamo dati veri
prepariamo API
testiamo DB

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    domain TEXT
);

Perché? ti serve qualcosa da leggere via API

inserisco dati

Cosa facciamo

mettiamo dati reali
simuliamo backend
testiamo query

Comando

INSERT INTO users (name, email, domain) VALUES ('Mario Rossi', 'mario@gmail.com', 'gmail.com'), ('Luca Bianchi', 'luca@libero.it', 'libero.it'), ('Anna Verdi', 'anna@outlook.com', 'outlook.com'), ('Paolo Neri', 'paolo@fastwebnet.it', 'fastwebnet.it');

Perché? senza dati non vedi nulla dopo

verifico

Comando

SELECT * FROM users;

Perché? confermi che il DB funziona


## COLLEGHIAMO FLASK AL DB - lavoro qui /var/www/devopsapp/backend

leggiamo i dati reali

esponiamo /users

installa libreria

pip install psycopg2-binary

oppure aggiungilo a requirements.txt: -> FACCIO COSI

psycopg2-binary

modifica app.py

versione minimale funzionante:

--

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="devopsdb",
        user="devopsuser",
        password="devopspassword"
    )

@app.route("/users")
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, email, domain FROM users;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "domain": row[3]
        })

    return jsonify(users)

--


rebuild

docker-compose down
docker-compose up -d --build

test

curl http://127.0.0.1/users

RISULTATO

[
  {"id":1,"name":"Mario Rossi",...},
  ...
]


-- qui con filtro sul dominio -> app.py

# ===== SCRIPT VECCHIO (SENZA DATABASE) =====
# from flask import Flask
# app = Flask(__name__)
#
# @app.route("/")
# def home():
#     return "DevOps Lab API Running"
#
# Questo era il primo script:
# - nessun database
# - risposta statica
# - solo test di funzionamento Flask


# ===== SCRIPT NUOVO (CON DATABASE + FILTRO) =====

import psycopg2  # libreria per connettersi a PostgreSQL
from flask import Flask, jsonify, request
# Flask = framework web
# jsonify = converte Python → JSON
# request = legge parametri dalla URL (es. ?domain=...)

app = Flask(__name__)  # crea l'app Flask


def get_db_connection():
    # funzione che apre connessione al database PostgreSQL

    return psycopg2.connect(
        host="db",
        # hostname Docker → nome servizio nel docker-compose (NON localhost)

        database="devopsdb",
        # nome del database creato nel container PostgreSQL

        user="devopsuser",
        # utente del database

        password="devopspassword"
        # password del database
    )


@app.route("/users")
# endpoint API accessibile via:
# http://localhost/users
# oppure:
# http://localhost/users?domain=gmail.com

def get_users():

    conn = get_db_connection()
    # apre connessione al database

    cur = conn.cursor()
    # crea cursore → oggetto che esegue query SQL


    # ===== VERSIONE VECCHIA (SENZA FILTRO) =====
    # cur.execute("SELECT id, name, email, domain FROM users;")
    # # prende tutti gli utenti dal database
    #
    # rows = cur.fetchall()
    # # recupera tutte le righe risultato


    # ===== VERSIONE NUOVA (CON FILTRO DINAMICO) =====

    domain = request.args.get("domain")
    # legge parametro dalla URL:
    # /users?domain=gmail.com
    # se non presente → None

    if domain:
        # se è presente il parametro domain

        cur.execute(
            "SELECT id, name, email, domain FROM users WHERE domain = %s;",
            (domain,)
        )
        # query SQL filtrata
        # %s = placeholder (sicuro → evita SQL injection)
        # (domain,) = valore passato alla query

    else:
        # se NON è presente filtro

        cur.execute("SELECT id, name, email, domain FROM users;")
        # prende tutti gli utenti


    rows = cur.fetchall()
    # prende risultati della query (filtrati o completi)


    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione DB


    users = []
    # lista vuota per costruire risposta JSON

    for row in rows:
        # per ogni riga del database

        users.append({
            "id": row[0],        # colonna id
            "name": row[1],      # colonna name
            "email": row[2],     # colonna email
            "domain": row[3]     # colonna domain
        })


    # ===== RISPOSTA API =====
    return jsonify(users)
    # restituisce JSON al client
    # (filtrato se ?domain=... presente, altrimenti completo)



curl "http://127.0.0.1/users?domain=gmail.com"


--

- cosi aggiungo user (POST)

curl -X POST http://127.0.0.1/users \
-H "Content-Type: application/json" \
-d '{"name":"Marco Test","email":"marco@gmail.com","domain":"gmail.com"}'



- cosi cancello DELETE

- sotto POST aggiungo 

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE id = %s RETURNING id;",
        (user_id,)
    )

    deleted_user = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if deleted_user:
        return jsonify({"message": "Utente eliminato"})
    else:
        return jsonify({"error": "Utente non trovato"}), 404
		
		
-- cosa fa?

riceve id
→ cerca utente
→ elimina dal DB
→ commit
→ restituisce risposta JSON


- elimino utente id 2

curl -X DELETE http://127.0.0.1/users/2

- se NGINX non risponde fare

docker-compose up -d

curl -X DELETE http://127.0.0.1/users/2

- continua a non funzionare

docker-compose down


curl -X DELETE http://127.0.0.1/users/2

- ora ok 

{"message":"Utente eliminato"}

-- flusso reale che ho appena fatto 

curl
→ nginx
→ backend
→ Flask DELETE endpoint
→ SQL DELETE
→ PostgreSQL
→ JSON response


- ora PUT 

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET name = %s, email = %s, domain = %s
        WHERE id = %s
        RETURNING id;
    """, (name, email, domain, user_id))

    updated_user = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if updated_user:
        return jsonify({"message": "Utente aggiornato"})
    else:
        return jsonify({"error": "Utente non trovato"}), 404
		
		
docker-compose down
docker-compose up -d --build

curl -X PUT http://127.0.0.1/users/1 \
-H "Content-Type: application/json" \
-d '{"name":"Mario Updated","email":"mario@gmail.com","domain":"gmail.com"}'


- CRUD aggiornato

FLUSSO 

Client
→ Nginx
→ Gunicorn
→ Flask API
→ PostgreSQL
→ volume persistente


VALIDATION

- aggiorno funzione POST

@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()
    # legge JSON dal body della richiesta

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")
    # prende i valori dal JSON

    # controllo campi mancanti/vuoti
    if not name or not email or not domain:
        return jsonify({
            "error": "Tutti i campi sono obbligatori"
        }), 400

    # controllo email base
    if "@" not in email:
        return jsonify({
            "error": "Email non valida"
        }), 400

    conn = get_db_connection()
    # apre connessione DB

    cur = conn.cursor()
    # crea cursore SQL

    cur.execute(
        "INSERT INTO users (name, email, domain) VALUES (%s, %s, %s);",
        (name, email, domain)
    )
    # inserisce dati nel DB (query parametrizzata)

    conn.commit()
    # salva modifiche (IMPORTANTISSIMO)

    cur.close()
    conn.close()
    # chiude connessione

    return jsonify({"message": "Utente creato"}), 201
    # risposta + status HTTP 201 (created)
	

-- TESTO ERRORE (fare rebuild)

curl -X POST http://127.0.0.1/users \
-H "Content-Type: application/json" \
-d '{"name":"Mario","email":"mariogmail.com","domain":"gmail.com"}'



REFACTOR 


Obiettivo

Passare da:

1 file gigante

a:

app.py
routes/
db/
Struttura nuova

Dentro:

/var/www/devopsapp/backend

crea:

mkdir routes
mkdir db
crea file route utenti
nano routes/users.py

Metti:

from flask import Blueprint, jsonify, request
# Blueprint = mini-router Flask
# jsonify = converte risposta in JSON
# request = legge dati in ingresso

from db.database import get_db_connection
# importa funzione connessione DB dal file separato

users_bp = Blueprint("users", __name__)
# crea blueprint dedicato alle route utenti


# ---------------- GET USERS ----------------

@users_bp.route("/users", methods=["GET"])
# endpoint GET /users

def get_users():

    conn = get_db_connection()
    # apre connessione PostgreSQL

    cur = conn.cursor()
    # crea cursore per eseguire query SQL

    cur.execute("SELECT id, name, email, domain FROM users;")
    # query che legge tutti gli utenti

    rows = cur.fetchall()
    # prende tutte le righe restituite dal DB

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione DB

    users = []
    # lista vuota che conterrà il JSON finale

    for row in rows:
        # ciclo su ogni record SQL

        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "domain": row[3]
        })
        # converte ogni riga SQL in dizionario JSON

    return jsonify(users)
    # restituisce lista utenti al client


# ---------------- POST USERS ----------------

@users_bp.route("/users", methods=["POST"])
# endpoint POST /users

def create_user():

    data = request.get_json()
    # legge JSON inviato dal client

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")
    # estrae campi dal JSON

    if not name or not email or not domain:
        # controlla campi mancanti

        return jsonify({
            "error": "Tutti i campi sono obbligatori"
        }), 400

    if "@" not in email:
        # controllo base email valida

        return jsonify({
            "error": "Email non valida"
        }), 400

    conn = get_db_connection()
    # apre connessione DB

    cur = conn.cursor()
    # crea cursore SQL

    cur.execute(
        "INSERT INTO users (name, email, domain) VALUES (%s, %s, %s);",
        (name, email, domain)
    )
    # inserisce nuovo utente nel DB

    conn.commit()
    # salva modifica nel DB

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione

    return jsonify({
        "message": "Utente creato"
    }), 201
    # restituisce conferma creazione

crea file db connection
nano db/database.py

Metti:

import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="devopsdb",
        user="devopsuser",
        password="devopspassword"
    )




ora puliamo app.py 

from flask import Flask
# importa framework Flask

from routes.users import users_bp
# importa blueprint utenti (route separate)

app = Flask(__name__)
# crea applicazione Flask principale

app.register_blueprint(users_bp)
# registra tutte le route presenti in users.py
# ora /users viene gestito dal blueprint



Architettura codice diventerà:

app.py = entry point
routes = endpoint
db = connessione DB


rebuild

docker-compose down
docker-compose up -d --build


TEST 

curl http://127.0.0.1/users


nano routes/users.py

- sotto POST metto 

# ---------------- DELETE USER ----------------

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
# endpoint DELETE /users/id

def delete_user(user_id):

    conn = get_db_connection()
    # apre connessione DB

    cur = conn.cursor()
    # crea cursore SQL

    cur.execute(
        "DELETE FROM users WHERE id = %s RETURNING id;",
        (user_id,)
    )
    # elimina utente tramite id

    deleted_user = cur.fetchone()
    # verifica se utente esisteva

    conn.commit()
    # salva modifica DB

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione

    if deleted_user:
        return jsonify({
            "message": "Utente eliminato"
        })

    else:
        return jsonify({
            "error": "Utente non trovato"
        }), 404


# ---------------- UPDATE USER ----------------

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
# endpoint PUT /users/id

def update_user(user_id):

    data = request.get_json()
    # legge JSON dal client

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")
    # estrae campi

    conn = get_db_connection()
    # connessione DB

    cur = conn.cursor()
    # cursore SQL

    cur.execute("""
        UPDATE users
        SET name = %s, email = %s, domain = %s
        WHERE id = %s
        RETURNING id;
    """, (name, email, domain, user_id))
    # aggiorna record utente

    updated_user = cur.fetchone()
    # verifica esistenza utente

    conn.commit()
    # salva update

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione

    if updated_user:
        return jsonify({
            "message": "Utente aggiornato"
        })

    else:
        return jsonify({
            "error": "Utente non trovato"
        }), 404


REBUILD

docker-compose down
docker-compose up -d --build


TEST 

curl -X DELETE http://127.0.0.1/users/6


curl http://127.0.0.1/users



***

HEALTHCHECK + LOGGING

- stato servizi
- monitoraggio
- runtime
- stdout/stderr
- docker logs
- osservabilità

vado in 'nano routes/users.py' e aggiungo 

# ---------------- HEALTHCHECK ----------------

@users_bp.route("/health", methods=["GET"])
# endpoint salute servizio

def healthcheck():

    return jsonify({
        "status": "ok",
        "service": "devopsapp-backend"
    }), 200

docker-compose down
docker-compose up -d --build

TEST

curl http://127.0.0.1/health

Questo è il primo concetto reale di:
- service health
- monitoring
- liveness
- readiness

che poi porta a:

- Kubernetes probes
- load balancer checks
- monitoring stack
- observability



*** LOGGING ***

inizio a vedere:

stdout
stderr
processi
docker logs
runtime behavior


Obiettivo: quando arriva una richiesta:

GET /users
POST /users
/health

voglio vedere log reali nel container.

nano backend/routes/users.py

aggiungo 'import logging'

creo logger

users_bp = Blueprint("users", __name__)
logger = logging.getLogger(__name__)
# crea logger del modulo corrente

-- il file diventa ... 

def healthcheck():

    logger.info("Healthcheck endpoint raggiunto")

    return jsonify({
        "status": "ok",
        "service": "devopsapp-backend"
    }), 200

--

TEST

curl http://127.0.0.1/health

docker ps

docker logs devopsapp-backend

E QUI arriva la parte importante

Sto vedendo:

stdout/stderr del processo gunicorn/python

cioè output runtime reale del container.cd