# Frequent Errors and Solutions

- In case if Postresql port is already in use: `systemctl stop postgresql`
- Port errors
```bash
# command to check port usage
export PORTNO=8088
sudo lsof -i -P -n | grep LISTEN | grep $PORTNO

#command to kill all running docker instances
docker kill $(docker ps -q) 
```

- `failed to dial gRPC: cannot connect to the Docker daemon. Is 'docker daemon' running on this host?: dial tcp 192.168.39.237:2376: connect: no route to host`
```
sudo service docker restart
```

- Image pull error
```
# try to use local images in dev environment
eval $(minikube docker-env)
```

- Stuck in `ContainerCreating` 
```
kubectl get events --all-namespaces  --sort-by='.metadata.creationTimestamp'
```