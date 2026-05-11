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


# ===== SCRIPT NUOVO (CON DATABASE + FILTRO) =====

import psycopg2  # libreria per connettersi a PostgreSQL
from flask import Flask, jsonify, request
# Flask = framework web
# jsonify = converte Python → JSON
# request = legge parametri dalla URL (es. ?domain=...)

app = Flask(__name__)  # crea l'app Flask


def get_db_connection():
    # funzione che apre connessione al database PostgreSQL

    return psycopg2.connect(
        host="db",  
        # hostname Docker → nome servizio nel docker-compose (NON localhost)

        database="devopsdb",  
        # nome del database creato nel container PostgreSQL

        user="devopsuser",  
        # utente del database

        password="devopspassword"  
        # password del database
    )


@app.route("/users")  
# endpoint API accessibile via:
# http://localhost/users
# oppure:
# http://localhost/users?domain=gmail.com

def get_users():

    conn = get_db_connection()  
    # apre connessione al database

    cur = conn.cursor()  
    # crea cursore → oggetto che esegue query SQL


    # ===== VERSIONE VECCHIA (SENZA FILTRO) =====
    # cur.execute("SELECT id, name, email, domain FROM users;")
    # # prende tutti gli utenti dal database
    #
    # rows = cur.fetchall()
    # # recupera tutte le righe risultato


    # ===== VERSIONE NUOVA (CON FILTRO DINAMICO) =====

    domain = request.args.get("domain")  
    # legge parametro dalla URL:
    # /users?domain=gmail.com
    # se non presente → None

    if domain:
        # se è presente il parametro domain

        cur.execute(
            "SELECT id, name, email, domain FROM users WHERE domain = %s;",
            (domain,)
        )
        # query SQL filtrata
        # %s = placeholder (sicuro → evita SQL injection)
        # (domain,) = valore passato alla query

    else:
        # se NON è presente filtro

        cur.execute("SELECT id, name, email, domain FROM users;")
        # prende tutti gli utenti


    rows = cur.fetchall()  
    # prende risultati della query (filtrati o completi)


    cur.close()  
    # chiude cursore

    conn.close()  
    # chiude connessione DB


    users = []  
    # lista vuota per costruire risposta JSON

    for row in rows:  
        # per ogni riga del database

        users.append({
            "id": row[0],        # colonna id
            "name": row[1],      # colonna name
            "email": row[2],     # colonna email
            "domain": row[3]     # colonna domain
        })


    # ===== RISPOSTA API =====
    return jsonify(users)  
    # restituisce JSON al client
    # (filtrato se ?domain=... presente, altrimenti completo)


@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()
    # legge JSON dal body della richiesta

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")
    # prende i valori dal JSON

    # controllo campi mancanti/vuoti
    if not name or not email or not domain:
        return jsonify({
            "error": "Tutti i campi sono obbligatori"
        }), 400

    # controllo email base
    if "@" not in email:
        return jsonify({
            "error": "Email non valida"
        }), 400

    conn = get_db_connection()
    # apre connessione DB

    cur = conn.cursor()
    # crea cursore SQL

    cur.execute(
        "INSERT INTO users (name, email, domain) VALUES (%s, %s, %s);",
        (name, email, domain)
    )
    # inserisce dati nel DB (query parametrizzata)

    conn.commit()
    # salva modifiche (IMPORTANTISSIMO)

    cur.close()
    conn.close()
    # chiude connessione

    return jsonify({"message": "Utente creato"}), 201
    # risposta + status HTTP 201 (created)



@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE id = %s RETURNING id;",
        (user_id,)
    )

    deleted_user = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if deleted_user:
        return jsonify({"message": "Utente eliminato"})
    else:
        return jsonify({"error": "Utente non trovato"}), 404


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET name = %s, email = %s, domain = %s
        WHERE id = %s
        RETURNING id;
    """, (name, email, domain, user_id))

    updated_user = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if updated_user:
        return jsonify({"message": "Utente aggiornato"})
    else:
        return jsonify({"error": "Utente non trovato"}), 404
