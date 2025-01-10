#!/bin/bash
docker build -t radac98/playlist-frontend:latest ./playlist-recommendation-system/frontend                                                
docker push radac98/playlist-frontend:latest

docker build -t radac98/playlist-backend:latest ./playlist-recommendation-system/backend
docker push radac98/playlist-backend:latest