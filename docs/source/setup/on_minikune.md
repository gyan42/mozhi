# Minikube

The demo is on local cluster using minikube, hence tunneling and port forwarding 
are used to access kubernetes service.

Required software packages:
- [Kubernetes command line tool](https://kubernetes.io/docs/tasks/tools/) : `kubectl`
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
  
- **Configs files used are placed in [mozhi/configs/](../../../configs)**

- Start minikube
```
# let minikube decided what works best fpr your machine setup
minikube start 
# if it failes try to use kvm2 as virtual machine  
minikube start  --vm-driver=kvm2

minikube addons enable ingress

alias km='kubectl -n mozhi'
```
- Install operators/helm charts
  - One time installation of [Kubegres Operator](https://www.kubegres.io/doc/getting-started.html)
  - Visit official [Krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/) for installation guide.

```
kubectl krew install minio
kubectl create namespace minio-operator
kubectl minio init --namespace minio-operator

kubectl apply -f https://raw.githubusercontent.com/reactive-tech/kubegres/v1.7/kubegres.yaml
```

- Create mozhi services
```
kubectl apply -f ops/k8s/mozhi/namespace.yaml
kubectl apply -f ops/k8s/mozhi/
kubectl apply -f ops/k8s/postgres/
kubectl apply -f ops/k8s/minio/
```
- Enable minikube tunnel for local access
```
# this needs a dedicated terminal to run in the background
minikube tunnel
```
- Get ingress address and add it to host machine for URL access
```
echo "$(kubectl get ingress -n mozhi | grep mozhi-api-ingress | cut -d' ' -f10) mozhi.ai"
# copy above line and add at the top of  /etc/hosts file
sudo vi /etc/hosts 
```
- Create required postgres user credentials and DB wth in `mozhi-postgres-db` container
```
kubectl exec -it service/mozhi-postgres-db -n mozhi -- bash
  >> psql -U postgres # mozhi
  >> CREATE USER mozhi WITH PASSWORD 'mozhi'; 
  >> CREATE DATABASE mozhidb; 
```
- Port forward postgresql service for [database preparation](prepare_data.md)
```
# this needs a dedicated terminal to run in the background
kubectl  port-forward service/mozhi-postgres-db 4321:5432 -n mozhi
```
- Port forward minio service for [image data and model preparation](prepare_data.md)
  [MinIO](https://localhost:9000/minio/)
  [MinIO-Console](https://localhost:9090/login)
```
# this needs a dedicated terminal to run in the background
# https://localhost:9000/
kubectl port-forward service/minio 9000:80 -n mozhi
```
Create alias : `mcli alias set mozhiminio http://localhost:9000 mozhi mozhi123`

- Port forward Torchserve
```
kubectl  port-forward service/mozhi-api-torchserve-svc 6543:6543 6544:6544 6545:6545  -n mozhi
```


```
# https://localhost:9090/
# this needs a dedicated terminal to run in the background
kubectl port-forward service/minio-console 9090:9443 -n mozhi
```  

- Misc commands
```
kubectl get all -n default
kubectl get all -n mozhi
kubectl get all -n kubegres-system

# to delete all objects in namespaces (be careful! it might delete your other objects)
kubectl delete all --all -n mozhi
kubectl delete all --all -n kubegres-system
kubectl delete all --all -n default
```