from flask import Flask
# framework Flask principale

from routes.users import users_bp
# importa blueprint users

app = Flask(__name__)
# crea applicazione Flask

app.register_blueprint(users_bp)
# registra endpoint blueprint users