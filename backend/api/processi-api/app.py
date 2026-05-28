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