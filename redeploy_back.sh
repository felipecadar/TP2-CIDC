#!/bin/bash
docker build -t radac98/playlist-frontend:1.0.0 ./playlist-recommendation-system/frontend                                                
docker push radac98/playlist-frontend:1.0.0

docker build -t radac98/playlist-backend:1.0.0 ./playlist-recommendation-system/backend
docker push radac98/playlist-backend:1.0.0

docker build -t radac98/playlist-ml-training:1.0.0 ./playlist-recommendation-system/ml-training
docker push radac98/playlist-ml-training:1.0.0