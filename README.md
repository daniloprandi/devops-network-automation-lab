DEVOPS NETWORK AUTOMATION LAB

AUTHOR
- ChatGPT (supporto strutturazione e revisione)
- Danilo Prandi

--------------------------------------------------

OVERVIEW

Questo progetto rappresenta un laboratorio DevOps costruito da zero con l’obiettivo di comprendere in modo pratico:

- infrastruttura Linux
- networking di base
- gestione servizi
- architettura backend
- flusso reale di una richiesta HTTP

Il focus principale non è solo far funzionare i servizi, ma capire come comunicano tra loro in un contesto simile alla produzione.

--------------------------------------------------

ARCHITETTURA

Il sistema è composto da:

CLIENT → NGINX → GUNICORN → FLASK
              ↑
           systemd

Descrizione:

- Il client (curl/browser) invia una richiesta HTTP
- NGINX riceve la richiesta sulla porta 80
- NGINX inoltra la richiesta al backend
- Gunicorn esegue l’applicazione Flask
- Flask processa la richiesta e restituisce la risposta
- systemd gestisce l’avvio automatico e la persistenza del servizio

--------------------------------------------------

COMPONENTI

NGINX
Web server e reverse proxy.
Gestisce l’accesso dall’esterno e inoltra le richieste al backend.

GUNICORN
Application server WSGI.
Esegue l’applicazione Flask in modo stabile e con gestione concorrente delle richieste.

FLASK
Backend API.
Gestisce routing, logica applicativa e risposta HTTP.

SYSTEMD
Service manager di Linux.
Permette avvio automatico, restart e monitoraggio del servizio.

--------------------------------------------------

STRUTTURA PROGETTO

/var/www/devopsapp
│
├── backend/
│   ├── venv/
│   └── app.py
│
├── docs/
│   └── architecture-metaphor.md
│
├── nginx/
│
└── README.md

--------------------------------------------------

GESTIONE SERVIZIO

Avvio:
sudo systemctl start devopsapp

Stato:
sudo systemctl status devopsapp

Restart:
sudo systemctl restart devopsapp

Log:
journalctl -u devopsapp -f

--------------------------------------------------

TEST

curl http://localhost

--------------------------------------------------

OBIETTIVO TECNICO

- Comprendere il flusso completo di una richiesta HTTP
- Distinguere tra web server e application server
- Gestire servizi Linux con systemd
- Preparare un ambiente simile alla produzione

--------------------------------------------------

SVILUPPI FUTURI

- Dockerizzazione del backend
- Containerizzazione NGINX
- Docker Compose
- Networking tra container
- Logging avanzato

--------------------------------------------------

NOTA

Questo progetto è stato sviluppato con un approccio pratico e progressivo, partendo da configurazioni manuali per costruire una comprensione reale dei componenti prima di passare alla containerizzazione.
