# ================================
# CONTAINER STATUS
# ================================

# verifica tutti i container attivi

docker ps


# verifica stato completo docker compose

docker compose ps



# ================================
# NGINX / REVERSE PROXY TEST
# ================================

# test endpoint processi-api
# passando attraverso nginx

curl http://127.0.0.1/health


# test dettagliato HTTP

curl -v http://127.0.0.1/health


# verifica logs nginx

docker logs devopsapp-nginx



# ================================
# PROCESSI-API TEST
# ================================

# verifica logs processi-api

docker logs devopsapp-processi-api


# verifica processi Linux
# dentro container processi-api

docker exec -it devopsapp-processi-api ps -ef


# verifica socket/porte
# dentro processi-api

docker exec -it devopsapp-processi-api ss -tulpn


# verifica interfacce rete container

docker exec -it devopsapp-processi-api ip addr



# ================================
# DOCKER INTERNAL NETWORK TEST
# ================================

# entra dentro container nginx

docker exec -it devopsapp-nginx sh


# test DNS Docker interno

ping processi-api


# test comunicazione nginx
# -> processi-api

curl http://processi-api:3140/health



# ================================
# DOCKER NETWORK ANALYSIS
# ================================

# lista reti Docker

docker network ls


# ispeziona rete backend

docker network inspect backend_default