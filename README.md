DEVOPS NETWORK AUTOMATION LAB | LABORATORIO DEVOPS — INFRASTRUTTURA, RETI E RUNTIME


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

- docker compose up -d --build

- verifica container:

  - docker ps

- Visualizzazione log:

  - docker logs NOME_CONTAINER

- Stop stack:

  - docker compose down


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