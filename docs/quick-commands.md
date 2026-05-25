# GITHUB 

cd $DEVOPSAPP_HOME

git status

git add .

git commit -m 'Porte api modificate'

git push origin main

# DOCKER

docker-compose down 
docker-compose up -d --build

# controllo container:

docker ps

# controllo logs processi-api:

docker logs devopsapp-processi-api

# test nginx:

curl http://127.0.0.1/health

# altri

docker-compose ps
docker-compose logs nginx