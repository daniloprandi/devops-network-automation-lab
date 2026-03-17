# 🚀 DevOps Lab – Flask + Nginx + systemd

## 📌 Obiettivo del progetto

Realizzare una mini infrastruttura reale con:

* Backend Python (Flask)
* Reverse Proxy (Nginx)
* Gestione servizio (systemd)
* Isolamento ambiente (virtualenv)

Obiettivo: simulare un'architettura base utilizzata in ambienti aziendali.

---

# 🧱 Architettura

```
Client (browser / curl)
        ↓
     Nginx (porta 80)
        ↓
 Reverse Proxy
        ↓
Flask App (127.0.0.1:5000)
        ↓
systemd (gestione servizio)
```

---

# ⚙️ Setup iniziale

## Aggiornamento sistema

```bash
sudo apt update
sudo apt upgrade -y
```

## Installazione componenti

```bash
sudo apt install python3 python3-venv python3-pip nginx -y
```

---

# 📁 Struttura progetto

```
/var/www/devopsapp/
└── backend/
    ├── app.py
    └── venv/
```

---

# 🐍 Backend Flask

## Creazione ambiente virtuale

```bash
cd /var/www/devopsapp/backend
python3 -m venv venv
source venv/bin/activate
pip install flask
```

---

## Codice applicazione (`app.py`)

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "DevOps Lab API Running"

@app.route("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
```

---

## Test manuale

```bash
python app.py
curl http://127.0.0.1:5000
```

---

# 🌐 Configurazione Nginx

## File config

```bash
sudo nano /etc/nginx/sites-available/devopsapp
```

## Contenuto

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Abilitazione sito

```bash
sudo ln -s /etc/nginx/sites-available/devopsapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Test Nginx

```bash
curl http://localhost
```

---

# 🔒 Sicurezza backend

Verifica che Flask NON sia esposto:

```bash
curl http://192.168.X.X:5000
```

Risultato atteso:

```
Connection refused
```

---

# ⚙️ Configurazione systemd

## Creazione servizio

```bash
sudo nano /etc/systemd/system/devopsapp.service
```

## Contenuto

```ini
[Unit]
Description=DevOps Flask API
After=network.target

[Service]
User=dprandi
WorkingDirectory=/var/www/devopsapp/backend
Environment="PATH=/var/www/devopsapp/backend/venv/bin"
ExecStart=/var/www/devopsapp/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Attivazione servizio

```bash
sudo systemctl daemon-reload
sudo systemctl start devopsapp
sudo systemctl enable devopsapp
```

---

## Verifica stato

```bash
sudo systemctl status devopsapp
```

Output atteso:

```
active (running)
```

---

## Log servizio

```bash
journalctl -u devopsapp -n 50 --no-pager
```

---

# 🧪 Test finale

## Backend (locale)

```bash
curl http://127.0.0.1:5000
```

## Nginx (entrypoint)

```bash
curl http://localhost
```

---

# 🔁 Test persistenza

```bash
sudo reboot
```

Dopo riavvio:

```bash
curl http://localhost
```

✔ L’app deve rispondere automaticamente

---

# 🧠 Concetti DevOps dimostrati

* Reverse Proxy (Nginx)
* Isolamento servizi (localhost)
* Gestione processi (systemd)
* Virtual Environment Python
* Architettura a livelli
* Debug e troubleshooting (porta occupata, restart loop)

---

# ⚠️ Note importanti

* Flask è un development server
* In produzione usare:

  * Gunicorn / uWSGI
* systemd elimina dipendenza da terminale
* Backend NON deve essere esposto direttamente

---

# 🚀 Prossimi sviluppi

* Gunicorn (production server)
* Dockerizzazione
* CI/CD pipeline
* Logging avanzato
* HTTPS (Let's Encrypt)

---

# 📌 Autori: IA (ChatGPT, Danilo Prandi)

DevOps Lab – percorso Infrastructure & Automation
Focus: Linux, Networking, Automation, Backend

---

