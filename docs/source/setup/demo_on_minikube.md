# Minikube

The demo is on local cluster using minikube, hence tunneling and port forwarding are used to access kubernetes service.

Required software packages:
- [Kubernetes command line tool](https://kubernetes.io/docs/tasks/tools/) : `kubectl`
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
  
- **Configs files used are placed in [mozhi/configs/](../../../configs)**

- Start minikube
```shell
# let minikube decided what works best fpr your machine setup
minikube start 
# if it failes try re run above command or use kvm2 as virtual machine on Ubuntu 
minikube start  --vm-driver=kvm2
minikube start --driver=virtualbox

minikube addons enable ingress

alias km='kubectl -n mozhi'

# To point your shell to minikube's docker-daemon, run:
eval $(minikube -p minikube docker-env)

# pull the images manually to avoid parallel pull error or network lags
docker pull mageswaran1989/mozhi-ui-cpu:latest
docker pull mageswaran1989/mozhi-api-cpu:latest
docker pull mageswaran1989/mozhi-ocr-cpu:latest
```

- Install operators/helm charts
  - One time installation of [Kubegres Operator](https://www.kubegres.io/doc/getting-started.html)
  - Visit official [Krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/) for installation guide.

```shell
kubectl krew install minio
kubectl create namespace minio-operator
kubectl minio init --namespace minio-operator

# Check above link for latest version
kubectl apply -f https://raw.githubusercontent.com/reactive-tech/kubegres/v1.12/kubegres.yaml
```
- Wait for few minutes till the system sets up the required services
- Create mozhi services
```shell
kubectl apply -f ops/k8s/mozhi/namespace.yaml

kubectl apply -f ops/k8s/postgres/
  > km get all # make sure postgres pods and services are up and running
  
kubectl apply -f ops/k8s/minio/
  > km get all # make sure minio pods and services are up and running
  
# following 
kubectl apply -f ops/k8s/mozhi/api.yaml
kubectl apply -f ops/k8s/mozhi/ocr.yaml
kubectl apply -f ops/k8s/mozhi/torch-serve.yaml

kubectl apply -f ops/k8s/mozhi/ui.yaml
kubectl apply -f ops/k8s/mozhi/ingress-controller.yaml
```

- Enable minikube tunnel for local access
```shell
# this needs a dedicated terminal to run in the background
minikube tunnel
```
- Get ingress address and add it to host machine for URL access
```shell
echo "$(kubectl get ingress -n mozhi | grep mozhi-api-ingress | cut -d' ' -f10) mozhi.ai"
# copy above line and add at the top of  /etc/hosts file
sudo vi /etc/hosts 
```
- Create required postgres user credentials and DB wth in `mozhi-postgres-db` container
```shell
kubectl exec -it service/mozhi-postgres-db -n mozhi -- bash
  >> psql -U postgres # mozhi
  >> CREATE USER mozhi WITH PASSWORD 'mozhi'; 
  >> CREATE DATABASE mozhidb; 
```
- Port forward postgresql service for [database preparation](prepare_data.md)
```shell
# this needs a dedicated terminal to run in the background
kubectl  port-forward service/mozhi-postgres-db 4321:5432 -n mozhi
```
- Port forward minio service for [image data and model preparation](prepare_data.md)
  [MinIO](https://localhost:9000/minio/)
  [MinIO-Console](https://localhost:9090/login)
```shell
# this needs a dedicated terminal to run in the background
# https://localhost:9000/
kubectl port-forward service/minio 9000:80 -n mozhi
```
Create alias : `mcli alias set mozhiminio http://localhost:9000 mozhi mozhi123`

- Port forward Torchserve
```shell
kubectl  port-forward service/mozhi-api-torchserve-svc 6543:6543 6544:6544 6545:6545  -n mozhi
```


```shell
# https://localhost:9090/
# this needs a dedicated terminal to run in the background
kubectl port-forward service/minio-console 9090:9443 -n mozhi
```  

- Misc commands
```shell
kubectl get all -n default
kubectl get all -n mozhi
kubectl get all -n kubegres-system

# to delete all objects in namespaces (be careful! it might delete your other objects)
kubectl delete all --all -n mozhi
kubectl delete all --all -n kubegres-system
kubectl delete all --all -n default
```