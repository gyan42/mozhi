# Kubernetes

Kubernetes is an open-source container-orchestration system for automating deployment, scaling and management of 
containerized applications.

[Install instructions](https://kubernetes.io/docs/tasks/tools/).

Minikube is a tool that makes it easy to run Kubernetes locally. Minikube runs a single-node Kubernetes cluster 
inside a VM on your laptop for users looking to try out Kubernetes or develop with it day-to-day.

## Minikube

[Official Setup Page](https://minikube.sigs.k8s.io/docs/start/)

**Linux Setup**
```bash
sudo apt-get install -y conntrack
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

**Mac Setup**
```bash
brew install minikube
# or
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

**Commands**

Note: `minikube start` fails in `docker-machine` environment. So, start the minikube first and then export the configs

```bash
# starts the pods in yor machine
# driver options: docker, virtualbox
export DRIVER=docker # dont export for it to figure out the best for your system
minikube start --nodes 4 --vm-driver=$(DRIVER) 

minikube stop

minikube dashboard

# delete local minikube node
minikube delete --all
```

**Addons**

```
#enable ingress contoller
minikube addons enable ingress
```

**Change owner and group**  
```
sudo chown -R $USER $HOME/.minikube
sudo chgrp -R $USER $HOME/.minikube
```

**Enable kubectl bash_completion**    
```
kubectl completion bash >>  ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion
```

**Alias**
```bash
alias k='kubectl'
alias km='kubectl -n mozhi'
alias kmd='kubectl -n mozhi describe'
```

**[Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)**

Some common commands that are handy while working with kubernetes.

```shell script
#to switch to minicube cluster context
kubectl config use-context minikube
kubectl get all -n kube-system

# list down all the pods 
kubectl get pods
# list all 
kubectl get all
# delete services
kubectl delete ${name from above list}
# delete all
kubectl delete all --all
# eg:
kubectl delete deployment.apps/spacy-flask-ner-python
# stop 
minikube stop
```


**References**

- https://medium.com/faun/how-to-restart-kubernetes-pod-7c702ca984c1
- [https://medium.com/@yzhong.cs/getting-started-with-kubernetes-and-docker-with-minikube-b413d4deeb92](https://medium.com/@yzhong.cs/getting-started-with-kubernetes-and-docker-with-minikube-b413d4deeb92)
- [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)
- [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/)
- [https://intellipaat.com/blog/tutorial/devops-tutorial/kubernetes-cheat-sheet/](https://intellipaat.com/blog/tutorial/devops-tutorial/kubernetes-cheat-sheet/)
- [Architecture]((https://www.edureka.co/blog/kubernetes-architecture/))
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux)
- [Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
- [Minikube Drivers](https://minikube.sigs.k8s.io/docs/drivers/)
    - [Docker](https://minikube.sigs.k8s.io/docs/drivers/docker/) 
    - [Hypervisor VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads)
        ```shell script
            sudo apt-get install libqt5opengl5
            sudo dpkg -i virtualbox-6.1_6.1.6-137129~Ubuntu~bionic_amd64.deb
        ```
- [Kubernetes YAML](https://www.mirantis.com/blog/introduction-to-yaml-creating-a-kubernetes-deployment/)
      
