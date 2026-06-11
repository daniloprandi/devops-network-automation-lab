# Flusso Sistema Distribuito DevOps Lab


## Scenario

VM3 esegue:

curl http://192.168.200.128/processi-api/processes


Obiettivo:

seguire una richiesta dal client fino al kernel Linux
e osservare il sistema tramite VM2.


---

# FLUSSO VM3 -> VM1


## 1) VM3 simulation-node

L'utente lancia curl.

Linux crea un processo:

curl
PID xxxx


## 2) Processo curl

curl costruisce:

GET /processi-api/processes

e prepara una richiesta HTTP.


## 3) Kernel VM3

curl usa le syscall di rete.

Linux crea una socket TCP.


## 4) Connessione TCP

Nasce:

VM3 porta random
        |
        v
VM1 porta 80


## 5) Incapsulamento rete

La richiesta diventa:

HTTP
 ↓
TCP segment
 ↓
IP packet
 ↓
Ethernet frame


## 6) VM1 serverlab-01

La scheda di rete riceve il frame.

Il kernel Linux ricostruisce i dati.


## 7) Porta 80

Linux vede:

destinazione TCP 80

e consegna al processo nginx.


## 8) Container nginx

Nginx riceve:

GET /processi-api/processes


## 9) Configurazione nginx

Legge:

nginx/default.conf

e cerca una location valida.


## 10) Routing nginx

Trova:

location /processi-api/

e inoltra la richiesta.


## 11) Docker network

La richiesta passa nella rete Docker.

Destinazione:

processi-api:3140


## 12) Container processi-api

Dentro gira:

Gunicorn


## 13) Gunicorn

Un worker riceve la richiesta.

La passa all'app Flask.


## 14) Flask

Flask cerca la route:

/processes

ed esegue la funzione Python.


## 15) Codice Python

La funzione usa moduli Linux.

Esempio:

os.listdir()


## 16) Filesystem /proc

Python legge:

/proc/PID/status


## 17) Kernel Linux

Il kernel restituisce:

- PID
- nome processo
- memoria
- stato
- thread


## 18) Creazione JSON

Flask prepara la risposta:

[
 {"pid":1}
]


## 19) Ritorno risposta

Percorso inverso:

Flask
 ↓
Gunicorn
 ↓
Nginx
 ↓
TCP/IP
 ↓
VM3 curl


## 20) Fine

curl stampa il JSON.

Il processo curl termina.



# FLUSSO VM2 -> VM1 (OBSERVABILITY)


## 1) VM2 observability-node

Esegue:

collector.py


## 2) Processo Python

Linux crea:

python3 PID xxxx


## 3) Collector

Ogni 5 secondi esegue:

requests.get()


## 4) Richiesta monitoring

Interroga:

VM1/processi-api/processes


## 5) VM1 risponde

Restituisce informazioni runtime Linux.


## 6) VM2 analizza

Riceve JSON.

Calcola metriche.


## 7) Futuro

Genererà:

- logs
- eventi
- anomalie
- security alert



# Schema finale


VM3
genera traffico

 ↓

VM1
riceve
processa
espone dati

 ↓

VM2
osserva
analizza
monitora