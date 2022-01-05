# mozhi API

## Setup Requirements
- [Deveploment Machine](dev_machine.md)

## Local Machine

```bash
python -m spacy download en_core_web_sm
cd /path/to/mozhi/
export DEBUG=true
api/start
```
[Check here for API Docs](http://localhost:8088/docs)

Test: 
```
curl http://0.0.0.0:8088

curl --location --request OPTIONS 'http://0.0.0.0:8088' --header 'Origin: http://mozhi.ai'

curl --location --request OPTIONS 'http://0.0.0.0:8088' \
--header 'Origin: http://mozhi.ai' \
--header 'Access-Control-Request-Method: POST' 

curl --location --request OPTIONS 'http://0.0.0.0:8088/vf/ner/model/spacy' --header 'Origin: http://mozhi.ai'


curl mozhi.ai/api/v1/

curl --header "Content-Type: application/json" --request POST --data '{"text":"Mozhi can solve NER problems"}' http://localhost:8088/vf/ner/model/spacy

kubectl exec service/mozhi-ui-cpu-svc --  curl --header "Content-Type: application/json" --request POST --data '{"text":"Mozhi can solve NER problems"}' http://mozhi.ai/mozhi/ner/model/spacy


curl --header "Content-Type: application/json" --request POST --data '{"text":"Mozhi can solve NER problems"}' http://a7f5567b110444e4cb445a71faee9b95-899e8adad051668a.elb.ap-south-1.amazonaws.com/api/v1/mozhi/ner/model/spacy

```

## Docker

`export VERSION=latest`

**With CPU only**

- [Dockerfile](../../../ops/docker/api/cpu/multistage/Dockerfile)
- Build  
`
docker build -t mozhi-api-cpu:latest -f ops/docker/api/cpu/multistage/Dockerfile .
`
- Debug  
```
docker container run -p 8088:8088 -it mozhi-api-cpu bash
docker container run -p 8088:8088 -it mageswaran1989/mozhi-api-cpu:latest bash
```
- Run Local Image  
`
docker container run -p 8088:8088 -it mozhi-api-cpu
`
- Run Dockerhub Image  
`
docker container run -p 8088:8088 -it mageswaran1989/mozhi-api-cpu:$VERSION
`
- Push to Dockerhub    
```
docker tag mozhi-api-cpu:latest mageswaran1989/mozhi-api-cpu:$VERSION
docker push mageswaran1989/mozhi-api-cpu:$VERSION

docker tag mozhi-api-cpu:latest mageswaran1989/mozhi-api-cpu:latest
docker push mageswaran1989/mozhi-api-cpu:latest
```

**With Nvidia GPU Support**
- [Dockerfile](../../../ops/docker/api/gpu/Dockerfile)
- Build  
`
docker build -t mozhi-api-gpu:latest -f ops/docker/api/gpu/Dockerfile .
`
- Debug  
`
docker container run --gpus all -it mozhi-api-gpu bash
`
- Run Local Image  
`
docker container run --gpus all -p 8088:8088 -it mozhi-api-gpu
`
- Run Dockerhub Image  
`
docker container run --gpus all -p 8088:8088 -it mageswaran1989/mozhi-api-gpu:0.1
`
- Push to Dockerhub    
```
docker tag mozhi-api-gpu:latest mageswaran1989/mozhi-api-gpu:$VERSION
docker push mageswaran1989/mozhi-api-gpu:$VERSION

docker tag mozhi-api-gpu:latest mageswaran1989/mozhi-api-gpu:latest
docker push mageswaran1989/mozhi-api-gpu:latest
```


## Kubernetes

[Ref1](https://github.com/4OH4/kubernetes-fastapi)

- Start  
`
kubectl apply -f ops/k8s/mozhi/api.yaml
`
- Debug
`
kubectl -n mozhi port-forward service/mozhi-api-cpu-svc 8088
`  
- Stop/Delete
`
kubectl delete pods,services,deployments,ingress -l org=mozhi   
`