from flask import Flask
# framework web Flask
#
# Flask riceve richieste HTTP
# e gestisce le route API

import os
# modulo Python standard
#
# permette interazione con:
# - filesystem
# - processi
# - sistema operativo Linux


app = Flask(__name__)
# crea l'app Flask principale


@app.route('/health')
# endpoint:
#
# GET /health
#
# usato per:
# - healthcheck
# - test container
# - verifica nginx reverse proxy
# - verifica runtime Flask

def health():

  return {

    'service': 'processi-api',
    # nome microservizio

    'status': 'running'
    # stato runtime applicazione
  }


@app.route('/processes')
# endpoint:
#
# GET /processes
#
# obiettivo:
# esporre processi Linux
# tramite pseudo-filesystem /proc

def processes():

  processi = os.listdir('/proc')
  # legge il contenuto di /proc
  #
  # /proc NON è un filesystem normale
  #
  # è un pseudo-filesystem
  # esposto direttamente dal kernel Linux
  #
  # contiene:
  # - processi
  # - cpu info
  # - memoria
  # - networking
  # - runtime kernel

  return {

    'processes': processi
    # ritorna contenuto /proc
    # come risposta JSON HTTP
  }


if __name__ == '__main__':
  # avvio locale Flask
  #
  # in produzione useremo Gunicorn

  app.run(

    host='0.0.0.0',
    # ascolta su tutte le interfacce container

    port=3140,
    # porta runtime processi-api

    debug=True
    # debug Flask attivo
  )