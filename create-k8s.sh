kind delete cluster --name k8s-submarine

# 1.15.6, 1.16.9, 1.17.5
kind create cluster --image kindest/node:v1.17.5 --name k8s-submarine
kubectl create namespace submarine
kubectl config set-context --current --namespace=submarine #set submarine as default namespace
kubectl apply -f ./dev-support/k8s/tfjob/crd.yaml
kubectl kustomize ./dev-support/k8s/tfjob/operator | kubectl apply -f -
kubectl apply -f ./dev-support/k8s/pytorchjob/

