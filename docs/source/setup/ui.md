# mozhi UI

[localhost:8080](localhost:8080)

## Setup Requirements
- [Deveploment Machine](dev_machine.md)

## Local Machine

```
cd /path/to/mozhi/
cd ui
yarn build
yarn serve
```

## Docker 

`export VERSION=0.3`

- [Dockerfile](../../../ops/docker/ui/Dockerfile)
- Build  
`
docker build -t mozhi-ui-cpu:latest -f ops/docker/ui/Dockerfile .
`
- Debug  
`
docker container run -it mozhi-api-cpu bash
`  
- Run Local Image  
`
docker container run -p 8080:80 -it mozhi-ui-cpu
`
- Run Dockerhub Image  
`
docker container run -p 8080:80 -it mageswaran1989/mozhi-ui-cpu:$VERSION
`
- Push to Dockerhub
```
docker tag mozhi-ui-cpu:latest mageswaran1989/mozhi-ui-cpu:$VERSION   
docker push mageswaran1989/mozhi-ui-cpu:$VERSION

docker tag mozhi-ui-cpu:latest mageswaran1989/mozhi-ui-cpu:latest
docker push mageswaran1989/mozhi-ui-cpu:latest
```

## Kubernetes

- Start
`
kubectl apply -f ops/k8s/services/ui.yaml
`
- Debug
```
minikube addons enable ingress
kubectl port-forward service/vf-ui-cpu-svc 8080:80
```
- Test back end API from UI pods
```
#Test accesing API pod from UI service pod  
kubectl exec service/vf-ui-cpu-svc  --  curl http://vf-api-cpu-svc:8088
kubectl exec service/vf-ui-cpu-svc --  curl --header "Content-Type: application/json" --request POST --data '{"text":"mozhi can solve NER problems"}' http://vf-api-cpu-svc:8088/vf/ner/model/spacy
  
#Test accesing API pod from API pod  
kubectl exec pod/vf-api-cpu-68bf8dcd69-q6lpf --  curl http://localhost:8088


kubectl exec pod/vf-api-cpu-68bf8dcd69-q6lpf -- curl --location --request OPTIONS 'http://localhost:8088' --header 'Origin: http://mozhi.ai'

kubectl exec service/vf-ui-cpu-svc -- curl --location --request OPTIONS 'http://vf-api-cpu-svc:8088/' --header 'Origin: http://mozhi.ai'
kubectl exec pod/vf-ui-cpu-85d4b7d768-bwx66 -- curl --location --request OPTIONS 'http://vf-api-cpu-svc:8088/' --header 'Origin: http://mozhi.ai'
kubectl exec pod/vf-ui-cpu-85d4b7d768-bwx66 -- curl --location --request OPTIONS 'http://vf-api-cpu-svc:8088/vf/ner/model/spacy' --header 'Origin: http://mozhi.ai'

# run the DNS lookup tool to resolve the Service name:
kubectl exec deployment.apps/vf-ui-cpu -- sh -c 'nslookup vf-api-cpu-svc | tail -n 5'
```

- Ingress Setup
```
kubectl get ingress

# NAME               CLASS    HOSTS         ADDRESS          PORTS   AGE
# minikube-ingress   <none>   mozhi.ai   192.168.39.143   80      2d8h
```
Add the following line to the bottom of the /etc/hosts file:    
    192.168.39.143 mozhi.ai

Test : `curl mozhi.ai`

- Stop/Delete
`
kubectl delete pods,services,deployments -l org=mozhi   
`  