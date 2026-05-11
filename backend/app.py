from flask import Flask
# importa framework Flask

from routes.users import users_bp
# importa blueprint utenti (route separate)

app = Flask(__name__)
# crea applicazione Flask principale

app.register_blueprint(users_bp)
# registra tutte le route presenti in users.py
# ora /users viene gestito dal blueprint
