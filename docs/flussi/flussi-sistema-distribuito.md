# Sistema distribuito - Flusso completo


## Ruoli nodi

### VM1 - serverlab-01

Ruolo:
- esegue applicazioni
- riceve richieste
- espone API


### VM2 - observability-node

Ruolo:
- osserva VM1
- raccoglie metriche
- esegue collector.py


### VM3 - simulation-node

Ruolo:
- genera traffico
- simula client


---

# Flusso VM3 -> VM1

1. VM3 esegue curl

Nasce un processo curl.


2. curl crea richiesta HTTP

GET /processi-api/processes


3. Linux VM3 crea socket TCP

Connessione verso VM1 porta 80.


4. VM1 riceve richiesta

Il kernel consegna a nginx.


5. nginx

Legge default.conf.

Inoltra verso processi-api.


6. Docker network

Trasporta verso:

processi-api:3140


7. Gunicorn

Riceve richiesta Flask.


8. Flask

Esegue endpoint Python.


9. processi-api

Legge:

/proc


10. Kernel Linux

Restituisce informazioni processi.


11. Risposta

JSON torna alla VM3.


---

# Flusso VM2 -> VM1

1. VM2 esegue:

collector.py


2. Il collector interroga:

processi-api


3. Riceve JSON


4. Analizza:

- processi
- metriche
- eventi


---

# Schema finale

VM3 genera

↓

VM1 esegue

↓

VM2 osserva