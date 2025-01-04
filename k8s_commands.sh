kubectl create namespace cadar
kubectl -n cadar apply -f /Users/cadar/Documents/Github/TP2-CIDC/playlist-recomendation-system/k8s/deployment.yaml
kubectl -n cadar apply -f /Users/cadar/Documents/Github/TP2-CIDC/playlist-recomendation-system/k8s/service.yaml
kubectl -n cadar get deployments
kubectl -n cadar get services