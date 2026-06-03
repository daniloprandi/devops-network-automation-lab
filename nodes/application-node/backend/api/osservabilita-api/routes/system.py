from flask import Blueprint, jsonify
# Blueprint = router Flask modulare
# jsonify = converte Python → JSON

import subprocess
# permette esecuzione comandi Linux runtime


system_bp = Blueprint("system", __name__)
# blueprint modulo system


# ---------------- HEALTHCHECK ----------------

@system_bp.route("/health", methods=["GET"])
# endpoint GET /health

def healthcheck():

  return jsonify({

    "status": "ok",
    # stato servizio

    "service": "osservabilita-api"
    # nome logico servizio

  }), 200


# ---------------- PROCESS LIST ----------------

@system_bp.route("/processes", methods=["GET"])
# endpoint GET /processes

def get_processes():

  result = subprocess.run(
    ["ps", "aux"],

    capture_output=True,
    # cattura stdout/stderr comando Linux

    text=True
    # converte output in stringa leggibile
  )

  # esegue comando Linux:
  # ps aux
  #
  # mostra processi runtime Linux


  return jsonify({

    "processes": result.stdout
    # stdout comando Linux

  })