FROM python:3.11-slim
# immagine Linux minimale con Python 3.11 già installato


WORKDIR /app
# directory di lavoro interna al container
# tutto il runtime API vivrà dentro /app


COPY api/processi-api .
# copia il codice della processi-api
#
# sorgente:
# backend/api/processi-api
#
# destinazione:
# /app dentro il container
#
# porta dentro:
# - app.py
# - requirements.txt
# - file del servizio


COPY common ./common
# copia il codice condiviso
#
# sorgente:
# backend/common
#
# destinazione:
# /app/common dentro il container
#
# contiene moduli riutilizzabili:
# - database
# - configurazioni future
# - utility future

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