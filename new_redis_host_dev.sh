#!/bin/bash

# If docker and docker compose is not installed please uncomment following lines
#echo "Installing Docker"
#curl -fsSL https://get.docker.com -o get-docker.sh
#sudo sh get-docker.sh
#sudo systemctl start docker

#echo "installing docker compose"
#sudo pip3 install docker compose

echo "Hosting Redis Database and Redis Insights"
sudo docker-compose -f ./redis_docker_compose_file/docker-compose.yml up -d