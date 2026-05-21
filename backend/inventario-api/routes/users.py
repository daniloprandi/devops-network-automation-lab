from flask import Blueprint, jsonify, request
# Blueprint = router Flask modulare
# jsonify = converte Python → JSON
# request = legge richieste HTTP

from db.database import get_db_connection
# importa funzione connessione PostgreSQL

users_bp = Blueprint("users", __name__)
# blueprint/router modulo users

# ---------------- GET USERS ----------------

@users_bp.route("/users", methods=["GET"])
# endpoint GET /users

def get_users():

    conn = get_db_connection()
    # apre connessione PostgreSQL

    cur = conn.cursor()
    # crea cursore SQL

    domain = request.args.get("domain")
    # legge eventuale filtro:
    # /users?domain=gmail.com

    if domain:
        # se filtro presente

        cur.execute(
            "SELECT id, name, email, domain FROM users WHERE domain = %s;",
            (domain,)
        )
        # query SQL filtrata

    else:
        # se nessun filtro presente

        cur.execute(
            "SELECT id, name, email, domain FROM users;"
        )
        # query completa

    rows = cur.fetchall()
    # prende risultati query

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione DB

    users = []
    # lista JSON finale

    for row in rows:
        # ciclo record SQL

        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "domain": row[3]
        })
        # converte riga SQL → JSON

    return jsonify(users)
    # restituisce risposta JSON

    # ---------------- CREATE USER ----------------

@users_bp.route("/users", methods=["POST"])
# endpoint POST /users

def create_user():

    data = request.get_json()
    # legge JSON dal body richiesta

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")
    # estrae campi JSON

    conn = get_db_connection()
    # apre connessione PostgreSQL

    cur = conn.cursor()
    # crea cursore SQL

    cur.execute(
        "INSERT INTO users (name, email, domain) VALUES (%s, %s, %s);",
        (name, email, domain)
    )
    # inserisce record nel database

    conn.commit()
    # salva modifiche DB

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione

    return jsonify({
        "message": "utente creato"
    }), 201
    # risposta HTTP 201 CREATED

    # ---------------- DELETE USER ----------------

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
# endpoint DELETE /users/id

def delete_user(user_id):

    conn = get_db_connection()
    # apre connessione PostgreSQL

    cur = conn.cursor()
    # crea cursore SQL

    cur.execute(
        "DELETE FROM users WHERE id = %s RETURNING id;",
        (user_id,)
    )
    # elimina utente tramite ID
    # RETURNING id verifica se utente esisteva

    deleted_user = cur.fetchone()
    # prende eventuale record eliminato

    conn.commit()
    # salva modifica DB

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione DB

    if deleted_user:
        # se utente esisteva

        return jsonify({
            "message": "utente eliminato"
        })

    else:
        # se utente non trovato

        return jsonify({
            "error": "utente non trovato"
        }), 404


# ---------------- UPDATE USER ----------------

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
# endpoint PUT /users/id

def update_user(user_id):

    data = request.get_json()
    # legge JSON body richiesta

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")
    # estrae campi JSON

    conn = get_db_connection()
    # apre connessione PostgreSQL

    cur = conn.cursor()
    # crea cursore SQL

    cur.execute("""
        UPDATE users
        SET name = %s,
            email = %s,
            domain = %s
        WHERE id = %s
        RETURNING id;
    """, (name, email, domain, user_id))
    # aggiorna record utente

    updated_user = cur.fetchone()
    # verifica se record esisteva

    conn.commit()
    # salva update DB

    cur.close()
    # chiude cursore

    conn.close()
    # chiude connessione DB

    if updated_user:
        # update riuscito

        return jsonify({
            "message": "utente aggiornato"
        })

    else:
        # utente inesistente

        return jsonify({
            "error": "utente non trovato"
        }), 404


# ---------------- HEALTHCHECK ----------------

@users_bp.route("/health", methods=["GET"])
# endpoint GET /health

def healthcheck():

    return jsonify({
        # converte dizionario Python → JSON

        "status": "ok",
        # stato servizio

        "service": "inventario-api"
        # nome logico API/container

    }), 200
    # risposta HTTP 200 OK