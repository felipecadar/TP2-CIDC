LOCAL_PATH_MODELS="$(pwd)/models"
LOCAL_PATH_DATASETS="$(pwd)/datasets"

echo -e "Starting minikube with the following paths mounted:\n"
echo -e "Models: ${LOCAL_PATH_MODELS}\n"
echo -e "Datasets: ${LOCAL_PATH_DATASETS}\n"

minikube start --mount --cpus=4 --memory=6000 --v=8
minikube mount ${LOCAL_PATH_MODELS}:/mnt/models &
minikube mount ${LOCAL_PATH_DATASETS}:/mnt/datasets &

echo -e "Minikube started!\n"