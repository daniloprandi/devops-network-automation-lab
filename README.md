📘 DEVOPS LAB – TIMELINE OPS COMPLETA
👤 Autori

IA (ChatGPT)

Danilo Prandi

🧭 OBIETTIVO DEL PROGETTO

Costruire e deployare un'applicazione Python in ambiente Linux utilizzando:

Flask (applicazione)

Gunicorn (application server)

Nginx (reverse proxy)

systemd (gestione servizio)

🧠 ARCHITETTURA FINALE
Client → Nginx → Gunicorn → Flask
                    ↑
                 systemd
📍 FASE 1 — CREAZIONE BACKEND (FLASK)
🔹 Definizione Flask

Flask è un framework web Python leggero che permette di creare API e applicazioni web.

Gestisce routing HTTP

Restituisce risposte al client

Usato per sviluppo

🔹 Codice applicazione
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "DevOps Lab API Running"

@app.route("/health")
def health():
    return jsonify(status="ok")
🔹 Comandi
python3 -m venv venv
source venv/bin/activate
pip install flask
python app.py
🎯 Risultato

App funzionante su 127.0.0.1:5000

Server Flask attivo (development)

📍 FASE 2 — INTRODUZIONE GUNICORN
🔹 Definizione Gunicorn

Gunicorn è un WSGI server che esegue applicazioni Python in produzione.

Gestisce worker process

Riceve richieste HTTP

Sostituisce Flask dev server

🔹 Problema affrontato

Errore:

Address already in use

👉 causa:

Flask già in esecuzione sulla porta 5000

🔹 Soluzione
sudo systemctl stop devopsapp
pkill gunicorn
🔹 Avvio corretto
gunicorn --bind 127.0.0.1:5000 app:app
🔹 Problema incontrato

request bloccata con curl

causa: working directory

🔹 Soluzione definitiva
gunicorn --chdir /var/www/devopsapp/backend \
--bind 127.0.0.1:5000 \
app:app
🎯 Risultato

Gunicorn attivo

API funzionante

Server production-ready

📍 FASE 3 — VIRTUALENV
🔹 Definizione

Ambiente isolato Python per gestire dipendenze.

🔹 Struttura
/var/www/devopsapp/backend/venv/
🔹 Binari importanti
venv/bin/gunicorn
venv/bin/python
🎯 Concetto chiave

systemd NON usa il virtualenv automaticamente
👉 bisogna usare path assoluti

📍 FASE 4 — SYSTEMD
🔹 Definizione

Sistema Linux per gestione servizi.

🔹 File service
[Service]
ExecStart=/var/www/devopsapp/backend/venv/bin/gunicorn \
--chdir /var/www/devopsapp/backend \
--bind 127.0.0.1:5000 \
app:app
🔹 Comandi
sudo systemctl daemon-reload
sudo systemctl start devopsapp
sudo systemctl enable devopsapp
systemctl status devopsapp
🔹 Problema affrontato

conflitto porta

processo manuale vs systemd

🔹 Soluzione

👉 eliminare processi manuali

pkill gunicorn
🎯 Risultato

servizio persistente

avvio automatico al boot

📍 FASE 5 — NGINX
🔹 Definizione

Web server e reverse proxy.

🔹 Concetto chiave
Nginx → inoltra richieste → Gunicorn

👉 backend NON esposto

🔹 Configurazione
server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
🎯 Risultato

accesso via localhost

separazione livelli

📍 FASE 6 — DEBUGGING REALE
🔹 Problemi affrontati
1. Porta occupata

causa: processo attivo

soluzione: stop/kill

2. Gunicorn non risponde

causa: working directory

soluzione: --chdir

3. systemd non parte

causa: porta occupata

soluzione: pulizia processi

4. PATH / eseguibili

gunicorn non trovato

soluzione: path assoluto o ./gunicorn

🎯 Competenze sviluppate

troubleshooting reale

gestione processi

debugging rete/app

📍 FASE 7 — TEST FINALE
🔹 Verifiche
systemctl status devopsapp
ps aux | grep gunicorn
ss -tulnp | grep 5000
curl http://127.0.0.1:5000
curl http://localhost
🔹 Test reboot
sudo reboot

👉 tutto funzionante dopo riavvio

🎯 RISULTATO FINALE

✔ Backend Python
✔ Gunicorn production server
✔ systemd gestione servizio
✔ Nginx reverse proxy
✔ Persistenza dopo reboot

🧠 COMPETENZE ACQUISITE

Linux server management

Process management (systemd)

Reverse proxy (Nginx)

Python backend (Flask)

Deployment con Gunicorn

Debugging infrastrutturale

💥 CONCLUSIONE

Questo progetto dimostra la capacità di:

deployare un'applicazione reale

gestire infrastruttura Linux

risolvere problemi tecnici reali
