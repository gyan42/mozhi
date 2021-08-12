# MinIO

## Setup

1. **Local**

Refer Install guide [here](https://min.io/download#/linux) and install both server and client using `deb` package method.

Note: The MinIO command line utility  has two aliases `mc` and `mcli`. Both are used interchageably by MinIO docs.

2. **Kubernetes**

MinIO Operator:s

```
alias km='kubectl -n mozhi'

kubectl krew update
kubectl krew install minio

kubectl create namespace minio-operator
kubectl minio init --namespace minio-operator
kubectl get all --namespace minio-operator

# To open Operator UI, start a port forward using this command: console http://localhost:9090
kubectl minio proxy -n minio-operator 

kubectl create namespace mozhi

kubectl apply -f ops/k8s/minio/mozhi-tiny-tenant.yaml
km get all
km get pvc
km get pv

kubectl port-forward service/minio 9000:443 --namespace mozhi
mcli alias set mozhiminio http://localhost:9000 mozhi mozhi

# delete
kubectl delete pvc -n mozhi $(kubectl get pvc --namespace mozhi | cut -d' ' -f1)
kubectl delete pv -n mozhi $(kubectl get pv --namespace mozhi | cut -d' ' -f1)
kubectl delete namespace mozhi

```
## Misc

- https://docs.min.io/docs/minio-admin-complete-guide.html

**Adding Keys**

```
mc alias set myminio http://192.168.0.142:9000 admin password
# or
mcli alias set myminio http://192.168.0.142:9000 BKIKJAA5BMMU2RHO6IBB V7f1CwQqAcwo80UEIJEjc5gVQUSSx5ohQ9GSrr12
```


Internal service name: YOURSERVICENAME.NAMESPACE.svc.cluster.local

**Password**
```
echo -n 'mozhi' | base64
echo -n 'bW96aGk=' | base64 -d

echo -n 'mozhi123' | base64
echo -n 'bW96aGkxMjM=' | base64 -d
```

### References
- https://docs.min.io/docs/deploy-minio-on-kubernetes.html
- https://github.com/minio/operator/blob/master/README.md
- https://www.olivercoding.com/2021-03-01-kubernetes-minio-init/
