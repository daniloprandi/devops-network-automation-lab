# 🚀 DevOps Lab – Flask, Gunicorn, Nginx, systemd

## 👤 Autori
- IA (ChatGPT)
- Danilo Prandi

---

## 🧭 Overview

Questo progetto dimostra il deploy di un'applicazione web Python utilizzando una architettura tipica in ambiente Linux.

### 🔧 Architettura

Client → Nginx → Gunicorn → Flask App  
            ↑  
          systemd  

---

## 🎯 Obiettivo

- Deploy di una web app Python in ambiente Linux
- Separazione tra sviluppo e produzione
- Gestione del servizio tramite systemd
- Utilizzo di reverse proxy (Nginx)
- Persistenza dopo reboot

---

## 🧠 Tecnologie utilizzate

### 🔹 Flask
Framework web leggero per Python utilizzato per creare API.

Funzionalità:
- Routing HTTP (`@app.route`)
- Gestione richieste/risposte
- Creazione endpoint REST

⚠️ Utilizzato solo per sviluppo (non produzione)

---

### 🔹 Gunicorn
WSGI server per eseguire applicazioni Python in produzione.

Funzionalità:
- Gestione processi worker
- Interfaccia tra web server e applicazione
- Performance e stabilità

✔ Sostituisce il server di sviluppo Flask

---

### 🔹 Nginx
Web server e reverse proxy.

Funzionalità:
- Riceve richieste HTTP
- Le inoltra al backend
- Migliora sicurezza e scalabilità

✔ Il backend non è esposto direttamente

---

### 🔹 systemd
Sistema di gestione servizi Linux.

Funzionalità:
- Avvio automatico servizi
- Restart automatico
- Gestione lifecycle processi

✔ Garantisce persistenza dopo reboot

---

## 📁 Struttura progetto


devopsapp/
├── backend/
│ ├── app.py
│ └── venv/
├── nginx/
├── docs/
├── index.html
└── README.md


---

## ⚙️ Applicazione Flask

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "DevOps Lab API Running"

@app.route("/health")
def health():
    return jsonify(status="ok")
🔧 Setup ambiente
Virtualenv
python3 -m venv venv
source venv/bin/activate
Installazione dipendenze
pip install flask gunicorn
🚀 Esecuzione
🔸 Modalità sviluppo
python app.py
🔸 Modalità produzione
gunicorn --bind 127.0.0.1:5000 app:app
⚙️ Configurazione systemd

File:

/etc/systemd/system/devopsapp.service
Contenuto:
[Unit]
Description=DevOps Flask API
After=network.target

[Service]
User=dprandi
WorkingDirectory=/var/www/devopsapp/backend

# Dev server (commentato)
# ExecStart=/var/www/devopsapp/backend/venv/bin/python app.py

# Production server
ExecStart=/var/www/devopsapp/backend/venv/bin/gunicorn --chdir /var/www/devopsapp/backend --bind 127.0.0.1:5000 app:app

Restart=always

[Install]
WantedBy=multi-user.target
🌐 Configurazione Nginx
server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
🧪 Test
curl http://127.0.0.1:5000
curl http://localhost
🔍 Debug e verifiche
systemctl status devopsapp
ps aux | grep gunicorn
ss -tulnp | grep 5000
🔁 Test persistenza
sudo reboot

Dopo reboot:

systemctl status devopsapp
🎯 Risultato finale

✔ Applicazione Flask funzionante
✔ Gunicorn configurato
✔ systemd attivo
✔ Nginx reverse proxy
✔ Servizio persistente

🧠 Competenze dimostrate

Linux server management

systemd

Nginx reverse proxy

Python / Flask

Gunicorn

Networking (127.0.0.1 vs esposizione)

Debugging infrastrutturale
