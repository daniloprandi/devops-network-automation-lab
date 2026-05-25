# my first api creation 

# vado in docker-compose e incollo

  processi-api:

    build:
      context: ./api/processi-api
      # cartella build processi-api

      dockerfile: Dockerfile
      # Dockerfile runtime servizio

    container_name: devopsapp-processi-api
    # nome container processi-api

    expose:
      - '3140'
      # porta visibile solo nella rete Docker

    restart: always
    # restart automatico container

# poi vado nel default.conf file di NGINX e metto sotto 'osservabilita-api'

    # ---------------- PROCESSI API ----------------

  location /health {

    proxy_pass http://processi-api:3140;
    # inoltra richieste healthcheck
    # verso processi-api

    proxy_set_header Host $host;

    proxy_set_header X-Real-IP $remote_addr;
  }

# poi creo dentro cartella api 

# - la cartella processi-api
# - dentro la cartella processi-api 
# - le 2 cartelle database e routes
# - il file di inizio app 'app.py'
# - il dockerfile in cui metto

# ***

# FROM python:3.11-slim
# immagine Linux minimale con Python 3.11 già installato


WORKDIR /app
# directory di lavoro interna al container
# tutto il runtime API vivrà dentro /app


COPY . .
# copia tutti i file locali
# dentro il filesystem del container

RUN apt-get update && apt-get install -y procps
# installa tool Linux:
# ps
# top 
# pgrep

RUN pip install --no-cache-dir -r requirements.txt
# installa dipendenze Python del servizio
#
# --no-cache-dir:
# evita cache pip inutile nel container
# → immagine più piccola


CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:3140", "app:app"]
# comando eseguito all'avvio container
#
# gunicorn:
# application server WSGI
#
# -w 3
# avvia 3 worker/processi Gunicorn
#
# -b 0.0.0.0:3140
# mette Gunicorn in ascolto
# sulla porta 3140 del container
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

# ***


# - il file requirements.txt (il minimo di risorse che serve all'api per funzionare) 

# a questo punto faccio la rebuild con docker 

docker compose down
docker compose up -d --build

# fino qui tutto ok, ho fatto in autonomia

# ora con AI

# creo api.py

from flask import Flask
# importa il framework Flask


app = Flask(__name__)
# crea l'applicazione Flask principale
#
# __name__:
# nome del modulo Python corrente
#
# Flask usa questa informazione per:
# - path interni
# - templates
# - static files
# - root application context


@app.route('/health')
# endpoint HTTP:
#
# GET /health
#
# route minima usata come:
# - healthcheck
# - test API
# - verifica container attivo
# - verifica reverse proxy nginx

def health():
  # funzione eseguita
  # quando arriva richiesta su /health

  return {

    'service': 'processi-api',
    # nome servizio/API

    'status': 'running'
    # stato runtime API
  }

# ora rebuild 

docker-compose down
docker-compose up -d --build

# ora testo 

curl http://127.0.0.1/health