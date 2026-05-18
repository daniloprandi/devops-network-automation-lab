from flask import Blueprint, jsonify, request
# Blueprint = mini-router Flask
# jsonify = converte risposta in JSON
# request = legge dati in ingresso

from db.database import get_db_connection
# importa funzione connessione DB dal file separato
import logging

users_bp = Blueprint("users", __name__)
# crea blueprint dedicato alle route utenti


# ---------------- GET USERS ----------------

@users_bp.route("/users", methods=["GET"])
# endpoint GET /users

def get_users():

    conn = get_db_connection()
    # apre connessione PostgreSQL

    cur = conn.cursor()
    # crea cursore per eseguire query SQL

    cur.execute("SELECT id, name, email, domain FROM users;")
    # query che legge tutti gli utenti

    rows = cur.fetchall()
    # prende tutte le righe restituite dal DB

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione DB

    users = []
    # lista vuota che conterrà il JSON finale

    for row in rows:
        # ciclo su ogni record SQL

        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "domain": row[3]
        })
        # converte ogni riga SQL in dizionario JSON

    return jsonify(users)
    # restituisce lista utenti al client


# ---------------- POST USERS ----------------

@users_bp.route("/users", methods=["POST"])
# endpoint POST /users

def create_user():

    data = request.get_json()
    # legge JSON inviato dal client

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")
    # estrae campi dal JSON

    if not name or not email or not domain:
        # controlla campi mancanti

        return jsonify({
            "error": "Tutti i campi sono obbligatori"
        }), 400

    if "@" not in email:
        # controllo base email valida

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
    # inserisce nuovo utente nel DB

    conn.commit()
    # salva modifica nel DB

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione

    return jsonify({
        "message": "Utente creato"
    }), 201
    # restituisce conferma creazione

# ---------------- DELETE USER ----------------

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
# endpoint DELETE /users/id

def delete_user(user_id):

    conn = get_db_connection()
    # apre connessione DB

    cur = conn.cursor()
    # crea cursore SQL

    cur.execute(
        "DELETE FROM users WHERE id = %s RETURNING id;",
        (user_id,)
    )
    # elimina utente tramite id

    deleted_user = cur.fetchone()
    # verifica se utente esisteva

    conn.commit()
    # salva modifica DB

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione

    if deleted_user:
        return jsonify({
            "message": "Utente eliminato"
        })

    else:
        return jsonify({
            "error": "Utente non trovato"
        }), 404


# ---------------- UPDATE USER ----------------

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
# endpoint PUT /users/id

def update_user(user_id):

    data = request.get_json()
    # legge JSON dal client

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")
    # estrae campi

    conn = get_db_connection()
    # connessione DB

    cur = conn.cursor()
    # cursore SQL

    cur.execute("""
        UPDATE users
        SET name = %s, email = %s, domain = %s
        WHERE id = %s
        RETURNING id;
    """, (name, email, domain, user_id))
    # aggiorna record utente

    updated_user = cur.fetchone()
    # verifica esistenza utente

    conn.commit()
    # salva update

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione

    if updated_user:
        return jsonify({
            "message": "Utente aggiornato"
        })

    else:
        return jsonify({
            "error": "Utente non trovato"
        }), 404

# ---------------- HEALTHCHECK ----------------
# endpoint usato per verificare se il servizio backend è vivo

@users_bp.route("/health", methods=["GET"])
# crea endpoint HTTP GET raggiungibile su /health

def healthcheck():
    # funzione eseguita quando arriva richiesta GET /health

    logger.info("Healthcheck endpoint raggiunto")
    # scrive log informativo
    
    return jsonify({
        # converte dizionario Python in risposta JSON

        "status": "ok",
        # indica che il servizio è operativo

        "service": "devopsapp-backend"
        # nome logico del backend/container

    }), 200
    # restituisce risposta HTTP 200 OK

    

users_bp = Blueprint("users", __name__)
logger = logging.getLogger(__name__)