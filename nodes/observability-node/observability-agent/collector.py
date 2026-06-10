# Libreria per fare richieste HTTP
# Il collector la usa per interrogare le API su VM1
import requests

# Libreria standard per gestire pause/intervalli
import time


# Endpoint esposto da serverlab-01 (VM1)
# Passaggio:
# VM2 -> nginx VM1 -> processi-api container
VM1_URL = "http://192.168.200.128/processi-api/processes"


# Ciclo infinito:
# un agent di monitoring normalmente resta sempre attivo
while True:

  print("Raccolta dati da serverlab-01...")

  # Invio richiesta HTTP GET verso VM1
  response = requests.get(VM1_URL)


  # Conversione risposta JSON in oggetto Python
  #
  # JSON:
  # [
  #   {"pid":1, "name":"systemd"},
  #   {"pid":20, "name":"nginx"}
  # ]
  #
  # diventa una lista Python di dizionari
  processes = response.json()


  # Prima metrica semplice:
  # quanti processi sono presenti sulla VM osservata
  process_count = len(processes)


  # Output osservazione
  print("Processi rilevati:", process_count)


  # Attesa prima della prossima raccolta
  time.sleep(5)