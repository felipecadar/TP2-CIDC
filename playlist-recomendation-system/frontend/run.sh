#!/bin/bash

# Set default port values if not provided
FRONTEND_PORT=${FRONTEND_PORT:-8080}
BACKEND_PORT=${BACKEND_PORT:-30502}

# Build the Docker container
docker build -t frontend .

# Run the container
docker run --rm -p $FRONTEND_PORT:80 -e BACKEND_PORT=$BACKEND_PORT frontend
