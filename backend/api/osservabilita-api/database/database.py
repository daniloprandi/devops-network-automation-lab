import psycopg2
# driver PostgreSQL


def get_db_connection():
    # apre connessione PostgreSQL

    return psycopg2.connect(

        host="db",
        # hostname container PostgreSQL
        # risolto dal DNS interno Docker

        database="devopsdb",
        # database PostgreSQL

        user="devopsuser",
        # utente DB

        password="devopspassword"
        # password DB
    )