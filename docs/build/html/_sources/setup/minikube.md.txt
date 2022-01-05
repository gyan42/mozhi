# Minikube

https://itnext.io/goodbye-docker-desktop-hello-minikube-3649f2a1c469

## Mac
```
brew install hyperkit
brew install docker
brew install kubectl
brew install minikube

minikube config set cpus 2
minikube config set memory 2g

minikube start --driver=hyperkit --container-runtime=docker --nodes 4

minikube start --driver=virtualbox --container-runtime=docker --nodes 4


minikube start --container-runtime=docker --nodes 4


minikube kubectl get nodes

eval $(minikube docker-env)

minikube addons enable ingress
minikube ip
minikube addons enable ingress-dns

minikube addons enable metallb

```