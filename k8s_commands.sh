# kubectl delete deployment playlist-recommender-deployment

# kubectl apply -f k8s/pv.yaml
# kubectl apply -f k8s/pvc.yaml
kubectl delete deployment playlist-recommender-deployment
kubectl delete service playlist-recommender-service
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get deployments
kubectl get services
