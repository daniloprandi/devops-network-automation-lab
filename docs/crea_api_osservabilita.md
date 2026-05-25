# cd /var/www/devopsapp/backend/api/osservabilita-api

mkdir routes
mkdir database
mkdir collectors

# creo i files

touch app.py

touch routes/system.py

touch database/database.py

touch Dockerfile

touch requirements.txt

# in requirements.txt metto questo. Serve a dichiarare le dipendenze Python del servizio e cioè: cosa serve all'app per esistere

flask
gunicorn
psycopg2-binary

**********************************************************************************************************
**********************************************************************************************************

# vado nel dockerfile 'backend/api/osservabilita-api/Dockerfile'.

FROM python:3.11-slim
# immagine Linux minimale con Python 3.11 già installato
#
# IMPORTANTISSIMO:
#
# container slim != sistema Linux completo
#
# il container contiene:
#
# - Python
# - librerie minime
# - filesystem minimale
#
# ma NON:
#
# - tool Linux completi
# - ps
# - top
# - netstat
#
# quindi alcune utility runtime
# vanno installate manualmente


WORKDIR /app
# directory di lavoro interna al container
# tutto il runtime API vivrà dentro /app


COPY . .
# copia tutti i file locali
# dentro il filesystem del container


RUN apt-get update && apt-get install -y procps
# installa utility Linux runtime
#
# procps contiene:
#
# - ps
# - top
# - pgrep
#
# necessario per:
#
# subprocess.run(["ps", "aux"])


RUN pip install --no-cache-dir -r requirements.txt
# installa dipendenze Python del servizio
#
# --no-cache-dir:
# evita cache pip inutile nel container
# → immagine più piccola


CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
# comando eseguito all'avvio container
#
# gunicorn:
# application server WSGI
#
# -w 3
# avvia 3 worker/processi Gunicorn
#
# -b 0.0.0.0:5000
# mette Gunicorn in ascolto
# sulla porta 5000 del container
#
# app:app
#
# primo "app":
# file app.py
#
# secondo "app":
# oggetto Flask:
#
# app = Flask(__name__)

**********************************************************************************************************
**********************************************************************************************************

# database/database.py

import psycopg2
# driver PostgreSQL


def get_db_connection():
    # apre connessione PostgreSQL

    return psycopg2.connect(

        host="db",
        # hostname container PostgreSQL
        # risolto dal DNS interno Docker

        database="devopsdb",
        # database PostgreSQL

        user="devopsuser",
        # utente DB

        password="devopspassword"
        # password DB
    )

**********************************************************************************************************
**********************************************************************************************************

# vado in routes/system.py

# e iniziamo con il primo endpoint runtime.

# Obiettivo Esporre: /health e poi: /processes

# dentro metto 

from flask import Blueprint, jsonify
# Blueprint = router Flask modulare
# jsonify = converte Python → JSON

import subprocess
# permette esecuzione comandi Linux runtime


system_bp = Blueprint("system", __name__)
# blueprint modulo system


# ---------------- HEALTHCHECK ----------------

@system_bp.route("/health", methods=["GET"])
# endpoint GET /health

def healthcheck():

    return jsonify({

        "status": "ok",
        # stato servizio

        "service": "osservabilita-api"
        # nome logico servizio

    }), 200


# ---------------- PROCESS LIST ----------------

@system_bp.route("/processes", methods=["GET"])
# endpoint GET /processes

def get_processes():

    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True
    )
    # esegue comando Linux:
    # ps aux
    #
    # capture_output=True
    # cattura stdout/stderr
    #
    # text=True
    # converte output in stringa leggibile

    return jsonify({

        "processes": result.stdout
        # stdout comando Linux

    })

**********************************************************************************************************
**********************************************************************************************************

# ora app.py 

# che diventa il bootstrap runtime della nuova API.

from flask import Flask
# framework Flask principale

from routes.system import system_bp
# importa blueprint system


app = Flask(__name__)
# crea applicazione Flask


app.register_blueprint(system_bp)
# registra blueprint system
# → abilita endpoint:
#
# /health
# /processes



**********************************************************************************************************
**********************************************************************************************************


<!-- STEP SUCCESSIVO
docker-compose.yml

Dobbiamo aggiungere:

osservabilita-api service

accanto a:

backend
nginx
db

Aggiungi questo blocco sotto backend:: -->

osservabilita-api:

  build:
    context: ./api/osservabilita-api
    # cartella build osservabilita-api

    dockerfile: Dockerfile
    # Dockerfile runtime servizio

  container_name: devopsapp-osservabilita-api
  # nome container

  expose:
    - "5000"
    # porta interna rete Docker

  restart: always
  # restart automatico container

IMPORTANTISSIMO

Ora hai davvero:

2 runtime Flask separati
2 container separati
2 processi Gunicorn separati


**********************************************************************************************************
**********************************************************************************************************



## Routing NGINX nuova API

A questo punto NGINX conosce solo:

- backend (inventario-api)

ma NON:

- osservabilita-api

Quindi bisogna aggiornare il reverse proxy.

---

## Obiettivo routing

Richieste:

/users

↓

inventario-api

---

Richieste:

/system
/processes
/health

↓

osservabilita-api

---

## Concetto architetturale

NGINX diventa:

- entry point HTTP unico
- traffic router tra servizi
- reverse proxy interno Docker

Quindi:

Client
→ NGINX
→ API corretta
→ risposta HTTP



# vado in nano /var/www/devopsapp/nginx/default.conf e AGGIUNGO 

 # ---------------- OSSERVABILITA API ----------------

  location /health {

    proxy_pass http://osservabilita-api:5000;
    # inoltra richieste healthcheck
    # verso osservabilita-api

    proxy_set_header Host $host;

    proxy_set_header X-Real-IP $remote_addr;
  }


  location /processes {

    proxy_pass http://osservabilita-api:5000;
    # inoltra richieste process runtime
    # verso osservabilita-api

    proxy_set_header Host $host;

    proxy_set_header X-Real-IP $remote_addr;
  }



**********************************************************************************************************
**********************************************************************************************************



# Integrazione nuova API nel runtime Docker

Dopo aver creato:

- app.py
- routes/
- database/
- Dockerfile
- requirements.txt

bisogna integrare il servizio
nell'infrastruttura runtime.

---

# Aggiornamento docker-compose

Aggiungere nuovo servizio:

osservabilita-api

nel file:

backend/docker-compose.yml

---

## Obiettivo

Creare:

- container dedicato
- runtime Gunicorn dedicato
- networking Docker dedicato

---

## Esempio struttura

osservabilita-api:

  build:
    context: ./api/osservabilita-api

    dockerfile: Dockerfile

  container_name: devopsapp-osservabilita-api

  expose:
    - "5000"

  restart: always

---

# Concetto architetturale

Ogni API diventa:

- processo separato
- container separato
- runtime separato
- servizio Docker separato

---

# Aggiornamento NGINX

NGINX deve conoscere
la nuova API.

Bisogna aggiornare:

nginx/default.conf

---

# Obiettivo routing

Richieste:

/users

↓

inventario-api

---

Richieste:

/system
/processes
/health

↓

osservabilita-api

---

# Concetto architetturale

NGINX diventa:

- entry point HTTP unico
- reverse proxy runtime
- traffic router tra container

---

# Esempio routing

location /processes {

  proxy_pass http://osservabilita-api:5000;

}

---

# Rebuild infrastruttura

Dopo modifiche:

docker-compose down

docker-compose up -d --build

---

# Cosa succede

Docker:

- builda nuova immagine
- crea nuovo container
- collega rete Docker
- avvia Gunicorn
- aggiorna runtime servizi

---

# Validazione runtime

Test endpoint:

curl http://127.0.0.1/health

curl http://127.0.0.1/processes

---

# Runtime debugging importante

Se compare:

500 Internal Server Error

bisogna leggere:

docker logs devopsapp-osservabilita-api

per vedere:

- stderr runtime
- traceback Python
- errori Linux/container

---

# Problema reale incontrato

Errore:

FileNotFoundError: 'ps'

---

# Motivo

Il container:

python:3.11-slim

NON contiene utility Linux complete.

Quindi:

subprocess.run(["ps", "aux"])

fallisce.

---

# Soluzione

Installare:

procps

nel Dockerfile.

---

# Obiettivo finale

Ottenere:

Client
→ NGINX
→ API corretta
→ Gunicorn
→ Flask
→ subprocess Linux
→ process table runtime
→ risposta HTTP

con:

- routing servizi
- networking Docker
- processi separati
- runtime modulari
- Linux observability