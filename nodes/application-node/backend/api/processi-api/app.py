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

from common.database import get_db_connection

app = Flask(__name__)
# crea l'app Flask principale

def save_process(processo):
  # salva un processo dentro PostgreSQL
  con = get_db_connection()
  # apre conessione database
  cur = con.cursor()
  # crea cursore SQL
  cur.execute("INSERT INTO processes(pid, name, state, ppid, threads, memory_kb) VALUES (%s, %s, %s, %s, %s, %s)",
    (
      processo['pid'],
      processo['name'],
      processo['state'],
      processo['ppid'],
      processo['threads'],
      processo['memory_kb']
    )
  )
  con.commit()
  # conferma INSERT
  cur.close()
  con.close()
  # chiude conessione

def read_process(pid):
  # legge informazioni di un processo Linux
  # usando /proc/<pid>/status

  path = f'/proc/{pid}/status'

  data = {
    'pid': pid,
    'name': None,
    'state': None,
    'ppid': None,
    'threads': None,
    'memory_kb': None
  }


  with open(path) as file:
    for line in file:
      if line.startswith('Name:'):
        data['name'] = line.split()[1]
      if line.startswith('State:'):
        data['state'] = line.split()[1]
      if line.startswith('PPid:'):
        data['ppid'] = int(line.split()[1])
      if line.startswith('Threads:'):
        data['threads'] = int(line.split()[1])
      if line.startswith('VmRSS:'):
        data['memory_kb'] = int(line.split()[1])
  return data

@app.route('/processes/collect', methods=['POST'])
# endpoint:
#
# POST /processes/collect
#
# obiettivo:
# raccogliere lo stato attuale
# dei processi Linux
#
# sorgente dati:
#
# /proc/<PID>/status
#
# destinazione:
#
# tabella PostgreSQL:
# processes

def collect_processes():
  con = get_db_connection()
  # apre conessione verso PostgreSQL
  #
  # usa:
  # common/database/conection.py

  cur = con.cursor()
  # crea un cursore SQL
  #
  # il cursore permette di:
  # - eseguire query
  # - inviare INSERT
  # - leggere risultati

  for pid in os.listdir('/proc'):
    # scorre tutti gli elementi
    # esposti dal kernel in /proc
    if not pid.isdigit():
      # scarta tutto ciò che
      # non rappresenta un processo
      #
      # tiene solo:
      #
      # /proc/1
      # /proc/7
      # /proc/100
      continue
    processo = read_process(pid)
    # legge:
    #
    # /proc/<PID>/status
    #
    # e restituisce:
    #
    # {
    #   pid,
    #   name,
    #   state,
    #   ppid,
    #   threads,
    #   memory_kb
    # }
    cur.execute(
      "INSERT INTO processes(pid, name, state, ppid, threads, memory_kb) VALUES (%s,%s,%s,%s,%s,%s)",
      # query SQL parametrizzata
      #
      # %s = placeholder gestiti da psycopg2
      #
      # evita concatenazione stringhe SQL
      (
        processo['pid'],
        # PID Linux
        processo['name'],
        # nome processo
        processo['state'],
        # stato processo:
        #
        # R = running
        # S = sleeping
        processo['ppid'],
        # parent process ID
        processo['threads'],
        # numero thread processo
        processo['memory_kb']
        # memoria residente usata
      )
    )


  con.commit()
  # conferma definitivamente
  # tutte le INSERT nel database
  cur.close()
  # chiude il cursore SQL
  con.close()
  # chiude la conessione PostgreSQL
  return {
    'status': 'ok',
    'total': len(
      [
        p for p in os.listdir('/proc')
        if p.isdigit()
      ]
    )
  }
  # risposta HTTP:
  #
  # conferma raccolta completata
  # e numero processi analizzati


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
# legge informazioni reali sui processi Linux
# tramite il filesystem virtuale /proc
#
# obiettivo futuro:
# salvare questi dati nella tabella:
#
# process_samples

def processes():

  processi = []
  # lista che rappresenta le future rows SQL

  elementi = os.listdir('/proc')
  # lettura directory /proc
  #
  # il kernel Linux espone qui:
  # - processi
  # - memoria
  # - cpu
  # - rete

  for e in elementi:
    # ciclo su tutti gli elementi presenti in /proc
    if e.isdigit():
      # ogni directory numerica rappresenta un processo
      #
      # esempio:
      #
      # /proc/1
      # /proc/8
      processo = {
        # struttura dati equivalente
        # alla futura r database

        'pid': e,
        'name': None,
        'state': None,
        'ppid': None,
        'threads': None,
        'memory_kb': None
      }


      status_file = f'/proc/{e}/status'
      # file virtuale creato dal kernel
      #
      # contiene lo stato del processo

      with open(status_file) as file:

        rows = file.readlines()
        # carica informazioni processo


      for r in rows:
        if r.startswith('Name:'):
          processo['name'] = r.split()[1]
          # nome processo
        elif r.startswith('State:'):
          processo['state'] = r.split()[1]
          # stato:
          #
          # R running
          # S sleeping

        elif r.startswith('PPid:'):

          processo['ppid'] = r.split()[1]
          # processo padre

        elif r.startswith('Threads:'):
          processo['threads'] = r.split()[1]
          # numero thread

        elif r.startswith('VmRSS:'):
          processo['memory_kb'] = r.split()[1]
          # memoria RAM residente in KB

      processi.append(processo)
      # aggiunta del record alla raccolta
  return {

    'total': len(processi),
    'processes': processi
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