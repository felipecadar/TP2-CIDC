# Build the Docker container
docker build -t ml-backend .

MODELS_PATH="../../models"
MODELS_PATH=$(realpath $MODELS_PATH)

PORT=5000

docker run --rm -p 30502:5000 -v "$MODELS_PATH":/app/models -e PORT=$PORT ml-backend
