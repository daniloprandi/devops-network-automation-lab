import psycopg2
# driver PostgreSQL
#
# permette ai servizi Python
# di comunicare con il database

def get_db_connection():
  # crea una connessione verso PostgreSQL
  con = psycopg2.connect(
    host='db',
    # nome servizio Docker PostgreSQL
    database='devopsdb',
    user='devopsuser',
    password='devopspassword'
  )

  return con