# DEVOPS NETWORK AUTOMATION LAB

## Laboratorio DevOps — Infrastructure, Networking e Linux Runtime


## Autore

Danilo Prandi  
ChatGPT (supporto strutturazione, revisione tecnica e documentazione)


---

# Panoramica

Questo progetto è un laboratorio pratico orientato allo studio dei sistemi.

L'obiettivo non è creare una semplice applicazione backend, ma costruire un ambiente reale dove osservare cosa succede sotto i diversi livelli di astrazione:

- applicazioni
- processi Linux
- runtime Python
- reverse proxy
- container Docker
- networking TCP/IP
- database
- filesystem
- kernel Linux

L'applicazione diventa uno strumento per osservare l'infrastruttura.


---

# Architettura generale


```text
CLIENT

  |
  | HTTP :80
  v

APPLICATION NODE
(serverlab01)

  |
  v

NGINX container
(reverse proxy)

  |
  | Docker Network
  v


+-------------------------------+

 Flask/Gunicorn Services


 inventario-api
 porta 5000


 osservabilita-api
 porta 4000


 processi-api
 porta 3140

        |
        |
        v

      /proc
        |
        v
   Linux Kernel


 PostgreSQL
 porta 5432

+-------------------------------+
```


---

# Nodi infrastrutturali


Il progetto è organizzato come un ambiente multi-nodo.


```text
nodes

├── application-node
│
├── observability-node
│
└── client-node
```


## application-node

Nodo attualmente implementato.

Contiene:

- API runtime
- NGINX
- Docker Compose
- database
- script di gestione sistema


## observability-node

Futuro nodo dedicato a:

- monitoring
- logging
- metriche
- tracing


## client-node

Futuro nodo per simulare:

- client
- traffico HTTP
- richieste di rete


---

# Alberatura progetto


```text
devopsapp

├── containers
│
├── docs
│
├── linux
│
├── networking
│
├── nodes
│   │
│   ├── application-node
│   │   │
│   │   ├── backend
│   │   │   │
│   │   │   ├── api
│   │   │   │
│   │   │   ├── inventario-api
│   │   │   ├── osservabilita-api
│   │   │   └── processi-api
│   │   │
│   │   ├── docker-compose.yml
│   │   │
│   │   ├── nginx
│   │   │
│   │   ├── deploy
│   │   │
│   │   └── scripts
│   │
│   ├── observability-node
│   │
│   └── client-node
│
└── README.md
```


---

# Container Docker


Container attuali:


```text
devopsapp-nginx

devopsapp-inventario-api

devopsapp-osservabilita-api

devopsapp-processi-api

PostgreSQL
```


---

# Componenti


## NGINX

Ruolo:

- reverse proxy
- punto ingresso HTTP
- instradamento verso API interne


---

## Gunicorn

Application server WSGI.

Gestisce:

- worker Python
- processi Flask
- richieste concorrenti


---

## Flask

Framework API.

Gestisce:

- routing HTTP
- endpoint
- logica dei servizi


---

## PostgreSQL

Database relazionale.

Gestisce:

- dati persistenti
- storage tramite volume Docker


---

## Docker

Layer di isolamento.

Gestisce:

- container
- immagini
- networking
- runtime


---

# API disponibili


## inventario-api


```text
/inventario-api
```

Gestione informazioni infrastrutturali.


---


## osservabilita-api


```text
/osservabilita-api
```

Raccolta dati e osservazione servizi.


---


## processi-api


```text
/processi-api/processes
```


Espone informazioni runtime Linux leggendo:

```text
/proc
```


Flusso:

```text
HTTP request

 ↓

Flask route

 ↓

Python os module

 ↓

/proc filesystem

 ↓

Linux Kernel
```


---

# Livelli studiati


Il laboratorio segue il percorso:


```text
HTTP

 ↓

NGINX

 ↓

Gunicorn

 ↓

Flask

 ↓

Docker

 ↓

Linux process

 ↓

/proc

 ↓

Kernel

 ↓

Networking

 ↓

Hardware
```


Obiettivo:

scendere progressivamente sotto ogni astrazione.


---

# Comandi principali


Avvio stack:


```bash
docker-compose up -d --build
```


Verifica container:


```bash
docker ps
```


Log:


```bash
docker logs nome_container
```


Stop:


```bash
docker-compose down
```


Test processi:


```bash
curl http://localhost/processi-api/processes
```


---

# Prossimi sviluppi


## Linux runtime

- leggere `/proc/PID/status`
- PID
- process state
- memoria
- parent process


## Docker internals

- namespace
- cgroups
- bridge network


## Networking

- socket
- TCP handshake
- tcpdump
- netstat / ss


## Observability

- metriche
- tracing
- logging
- eBPF


---

# Filosofia del progetto


Questo laboratorio non studia solamente come creare servizi software.

Studia cosa succede sotto:

- quando nasce un processo
- come comunica un servizio
- come viaggia una richiesta HTTP
- come Docker isola un runtime
- come Linux espone informazioni interne

L'obiettivo finale è comprendere l'intero percorso:

```text
Codice

 ↓

Runtime

 ↓

Sistema operativo

 ↓

Kernel

 ↓

Hardware







# ======================================================================================================================================
# ======================================================================================================================================  #====================================================================================================================================== 



<!-- DEVOPS NETWORK AUTOMATION LAB | LABORATORIO DEVOPS — INFRASTRUTTURA, RETI E RUNTIME


AUTORE

- Danilo Prandi
- ChatGPT (supporto strutturazione, revisione tecnica e documentazione)


PANORAMICA

Questo progetto è un laboratorio pratico costruito per comprendere cosa accade realmente sotto i vari livelli di un’applicazione backend moderna containerizzata.

L’obiettivo non è soltanto sviluppare una REST API, ma osservare e capire come comunicano tra loro:

- processi Linux

- servizi backend

- reverse proxy

- container Docker

- rete TCP/IP

- database

- filesystem

- runtime applicativi


L’applicazione viene utilizzata come ambiente reale di sperimentazione per scendere progressivamente sotto le astrazioni software e infrastrutturali.

ARCHITETTURA

Client→ NGINX→ Gunicorn→ Flask API→ PostgreSQL→ Docker Volume

Tutti i componenti girano all’interno di container Docker collegati tramite una rete privata isolata.


FLUSSO DI UNA RICHIESTA HTTP

- Il client invia una richiesta HTTP

- NGINX riceve il traffico sulla porta 80

- NGINX agisce come reverse proxy

- La richiesta viene inoltrata al backend Flask/Gunicorn

- Flask esegue la logica applicativa

- PostgreSQL esegue le query SQL

- La risposta JSON torna al client tramite NGINX


ARCHITETTURA DOCKER

Container presenti:

- nginx

- backend (Flask + Gunicorn)

- db (PostgreSQL)

Componenti Docker utilizzati:

- Docker Compose

- rete Docker isolata

- volumi persistenti

Il database PostgreSQL non è esposto direttamente all’esterno.

La comunicazione avviene esclusivamente tramite la rete interna Docker.

COMPONENTI PRINCIPALI


- NGINX

  - reverse proxy

  - punto di ingresso HTTP

  - gestione traffico verso backend


- GUNICORN

  - application server WSGI

  - gestione concorrente delle richieste

  - runtime server per Flask


- FLASK

  - API backend

  - routing HTTP

  - logica applicativa

  - comunicazione database


- POSTGRESQL

  - database relazionale

  - esecuzione query SQL

  - persistenza dati


- DOCKER

  - isolamento servizi

  - networking tra container

  - runtime infrastrutturale


- ENDPOINT API


devops-network-automation-lab/
│
├── backend/
│   │
│   ├── api/
│   │   │
│   │   ├── inventario-api/
│   │   │   │
│   │   │   ├── database/
│   │   │   │
│   │   │   ├── models/
│   │   │   │
│   │   │   ├── routes/
│   │   │   │
│   │   │   ├── services/
│   │   │   │
│   │   │   ├── app.py
│   │   │   │
│   │   │   ├── Dockerfile
│   │   │   │
│   │   │   └── requirements.txt
│   │   │
│   │   ├── osservabilita-api/
│   │   │   │
│   │   │   ├── database/
│   │   │   │
│   │   │   ├── routes/
│   │   │   │
│   │   │   ├── services/
│   │   │   │
│   │   │   ├── utils/
│   │   │   │
│   │   │   ├── app.py
│   │   │   │
│   │   │   ├── Dockerfile
│   │   │   │
│   │   │   └── requirements.txt
│   │   │
│   │   └── processi-api/
│   │       │
│   │       ├── routes/
│   │       │
│   │       ├── services/
│   │       │
│   │       ├── utils/
│   │       │
│   │       ├── app.py
│   │       │
│   │       ├── Dockerfile
│   │       │
│   │       └── requirements.txt
│   │
│   └── venv/
│       │
│       ├── bin/
│       ├── lib/
│       ├── lib64/
│       └── pyvenv.cfg
│
├── deploy/
│   │
│   ├── devopsapp.service
│   │
│   └── scripts/
│       │
│       ├── start.sh
│       ├── restart.sh
│       └── healthcheck.sh
│
├── docs/
│   │
│   ├── networking/
│   ├── docker/
│   ├── tcp/
│   └── observability/
│
├── nginx/
│   │
│   ├── default.conf
│   │
│   └── logs/
│
├── data/
│   │
│   ├── postgres/
│   │
│   └── logs/
│
├── docker-compose.yml
│
├── .env
│
├── .gitignore
│
├── index.html
│
└── README.md


LIVELLI DI ASTRAZIONE ESPLORATI

Questo laboratorio viene utilizzato per esplorare progressivamente diversi livelli infrastrutturali:

- HTTP→ Reverse Proxy→ Runtime WSGI→ Flask Routing→ SQL→ PostgreSQL→ Docker Networking→    Processi Linux→ TCP/IP→ Isolamento Container→ Persistenza Filesystem

L’obiettivo è comprendere cosa accade sotto ogni layer dell’applicazione e dell’infrastruttura:

- avvio dello stack

- avvio servizi

- docker-compose up -d --build

- verifica container:

  - docker ps

- Visualizzazione log:

  - docker logs NOME_CONTAINER

- Stop stack:

  - docker-compose down


TEST API

Lista utenti:

- curl http://127.0.0.1/users

Creazione utente:

- curl -X POST http://127.0.0.1/users \-H "Content-Type: application/json" \-d '{"name":"Mario","email":"mario@gmail.com","domain":"gmail.com"}'


OBIETTIVI TECNICI

- comprendere il ciclo completo di una richiesta HTTP

- distinguere web e application server

- analizzare networking tra container

- comprendere runtime e processi backend

- osservare comunicazione tra servizi

- gestire persistenza dati containerizzata

- costruire un ambiente backend modulare e isolato


PROSSIMI PASSI

- variabili ambiente (.env)

- logging centralizzato

- healthcheck servizi

- monitoring

- redis caching

- pipeline CI/CD

- tracing

- docker internals

- network inspection

- namespaces

- cgroups

- osservabilità eBPF


NOTA FINALE

Questo laboratorio segue un approccio progressivo orientato all’infrastruttura, all’osservabilità dei sistemi e alla comprensione dei livelli sottostanti.

Ogni componente viene introdotto per capire:

- cosa fa

- come comunica

- quale layer rappresenta

- cosa esiste sotto di esso


L’applicazione backend viene utilizzata come ambiente reale per esplorare networking, runtime, processi Linux, containerizzazione e comportamento dei servizi distribuiti.

L’obiettivo non è costruire una semplice applicazione CRUD, ma utilizzare il software come strumento per osservare l’infrastruttura stessa.

Il laboratorio evolve quindi verso un modello in cui:

- l’infrastruttura osserva l’infrastruttura

- i processi osservano altri processi

- i servizi generano telemetria sui servizi

- il networking viene studiato attraverso traffico reale

- il runtime Linux diventa parte integrante dell’osservazione

L’intero progetto è pensato come un percorso progressivo per scendere sotto ogni astrazione software fino ai meccanismi reali del sistema operativo, del networking e del runtime Linux. -->