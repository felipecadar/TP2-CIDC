#!/bin/bash

# Usage: ./train.sh /path/to/dataset

DATASET_PATH="../../datasets"
MODELS_PATH="../../models"
# DATASET_PATH=$1
# MODELS_PATH=$2

# make it into absolute path
DATASET_PATH=$(realpath $DATASET_PATH)
MODELS_PATH=$(realpath $MODELS_PATH)


# Build the Docker container
docker build -t ml-training .

# make container

docker run --rm \
    -v "$DATASET_PATH":/app/dataset \
    -v "$MODELS_PATH":/app/models \
    -w /app \
    ml-training \
    python train.py --input-dataset /app/dataset/2023_spotify_ds1.csv --output /app/models --min-support 0.05 --min-confidence 0.5
