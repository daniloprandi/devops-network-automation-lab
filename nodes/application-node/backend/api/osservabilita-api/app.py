from flask import Flask
# framework Flask principale

from routes.system import system_bp
# importa blueprint system


app = Flask(__name__)
# crea applicazione Flask


app.register_blueprint(system_bp)
# registra blueprint system
# → abilita endpoint:
#
# /health
# /processes