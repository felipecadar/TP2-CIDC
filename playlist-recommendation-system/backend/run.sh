# Build the Docker container
docker build -t ml-backend .

MODELS_PATH="../../models"
DATASET_PATH="../../datasets"
MODELS_PATH=$(realpath $MODELS_PATH)
DATASET_PATH=$(realpath $DATASET_PATH)

PORT=52019

docker run --rm \
    -p 52019:52019 \
    -v "$MODELS_PATH":/app/models \
    -v "$DATASET_PATH":/app/dataset \
    -e PORT=$PORT \
    ml-backend
