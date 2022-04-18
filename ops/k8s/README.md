# Kubernetes Cluster Setup

k create ns mozhi
km apply -f ../local-storage-volume.yaml
helm install ts . --namespace mozhi

helm uninstall ts . --namespace mozhi
km delete -f ../local-storage-volume.yaml
