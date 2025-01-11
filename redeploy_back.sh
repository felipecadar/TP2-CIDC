#!/bin/bash

VERSION=1.0.5

docker build -t quay.io/radac98/playlist-frontend:$VERSION ./playlist-recommendation-system/frontend                                                
docker push quay.io/radac98/playlist-frontend:$VERSION

docker build -t quay.io/radac98/playlist-backend:$VERSION ./playlist-recommendation-system/backend
docker push quay.io/radac98/playlist-backend:$VERSION

docker build -t quay.io/radac98/playlist-ml-training:$VERSION ./playlist-recommendation-system/ml-training
docker push quay.io/radac98/playlist-ml-training:$VERSION