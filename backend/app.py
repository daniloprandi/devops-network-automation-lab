# ===== SCRIPT VECCHIO (SENZA DATABASE) =====
# from flask import Flask
# app = Flask(__name__)
#
# @app.route("/")
# def home():
#     return "DevOps Lab API Running"
#
# Questo era il primo script:
# - nessun database
# - risposta statica
# - solo test di funzionamento Flask

# ===== SCRIPT NUOVO (CON DATABASE) =====

import psycopg2  # libreria per connettersi a PostgreSQL
from flask import Flask, jsonify  # Flask = framework, jsonify = converte in JSON

app = Flask(__name__)  # crea l'app Flask

def get_db_connection():
    # funzione che apre connessione al database
    return psycopg2.connect(
        host="db",  # hostname Docker (nome servizio nel docker-compose)
        database="devopsdb",  # nome database
        user="devopsuser",  # utente DB
        password="devopspassword"  # password DB
    )

@app.route("/users")  # endpoint API accessibile via /users
def get_users():
    conn = get_db_connection()  # apre connessione DB
    cur = conn.cursor()  # crea cursore per eseguire query

    cur.execute("SELECT id, name, email, domain FROM users;")  # query SQL
    rows = cur.fetchall()  # prende tutte le righe risultato

    cur.close()  # chiude cursore
    conn.close()  # chiude connessione DB

    users = []  # lista vuota per costruire risposta JSON

    for row in rows:  # per ogni riga del DB
        users.append({
            "id": row[0],        # colonna id
            "name": row[1],      # colonna name
            "email": row[2],     # colonna email
            "domain": row[3]     # colonna domain
        })

    return jsonify(users)  # restituisce JSON al client
