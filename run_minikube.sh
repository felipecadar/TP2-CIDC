LOCAL_PATH_MODELS="$(pwd)/models"
LOCAL_PATH_DATASETS="$(pwd)/datasets"

mkdir -p ./volume
FULL_PATH_VOLUME="$(pwd)/volume"

minikube delete
minikube start --mount --cpus=4 --memory=6000 --v=8 --mount --mount-string="$FULL_PATH_VOLUME:/mnt/volume"
echo -e "Minikube started!\n"

if minikube ssh "ls /mnt" | grep -q "volume"; then
    echo "Volume creation successful!"
else
    echo "Volume creation failed!"
fi
