# Docker

## 1. Setup
- https://hub.docker.com/r/nvidia/cuda
- https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker
- [https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
- [https://docs.docker.com/engine/reference/builder/](https://docs.docker.com/engine/reference/builder/)

**[Mac Setup](https://apple.stackexchange.com/questions/373888/how-do-i-start-the-docker-daemon-on-macos)**

```shell
docker-machine create --driver virtualbox default
docker-machine restart
eval "$(docker-machine env default)"

docker-machine rm default
```
**docker cli**

```shell
sudo apt  install docker.io

sudo systemctl start docker
sudo systemctl enable docker
docker --version

# Put the user in the docker group
newgrp docker
sudo usermod -a -G docker $USER
```

**docker-compose cli**

https://docs.docker.com/compose/install/

```
docker-compose --version
```

**Nvidia container toolkit**

Nvidia has prebuild iamges for GPU support inside the container, which can be used with 
`nvidia-container-toolkit` 

Note : The prebuild images are huge `~10GB`

```
sudo apt install curl
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Check Docker image
docker run --gpus all nvidia/cuda:10.2-base nvidia-smi

## Running GUI Applications
xhost +local:docker
docker run --gpus all -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    nathzi1505:darknet bash
```

**How to fix SSD Disk Space Constraints?**

Docker image builds will eat up lot of disk space, it is ideal to use HDD instead of SSD in case if you happened to have one! 
Below are the steps to update the `root folder` of Docker download path to parquet the files.

```
sudo systemctl stop docker

sudo mv /var/lib/docker/ /opt/binaries/
sudo rm -rf /var/lib/docker
sudo ln -s /opt/binaries/docker/ /var/lib/docker

sudo vim /etc/docker/daemon.json\:

    {
        “data-path”: “/opt/binaries/docker”,
        “graph”: “/opt/binaries/docker”
    } 

sudo systemctl daemon-reload
sudo systemctl restart docker

sudo ls /opt/binaries/docker
    mageswarand@IMCHLT276:/opt/binaries/docker$ ls
    builder  buildkit  containers  image  network  overlay2  plugins  runtimes  swarm  tmp  trust  volumes

```
docker container top f1

In case if you face any face network issues with docker, 
refer [https://pythonspeed.com/articles/docker-connection-refused/](https://pythonspeed.com/articles/docker-connection-refused/)


## 2. Misc 

**Image Size Analysis**
```
# https://github.com/wagoodman/dive
wget https://github.com/wagoodman/dive/releases/download/v0.9.2/dive_0.9.2_linux_amd64.deb
sudo apt install ./dive_0.9.2_linux_amd64.deb

dive <your-image-tag>
```

**Common commands**

- https://www.edureka.co/blog/docker-commands/

- start the services
```
sudo service docker start
or 
systemctl start docker
systemctl enable docker
```

- build the image
```
docker build --network host -f docker/api/Dockerfile -t spacy-flask-ner-python:latest .
```

- run docker in interactive mode
```
docker run -ti spacy-flask-ner-python /bin/bash
```

- start the app
```
docker run -d -p 5000:5000 spacy-flask-ner-python
```

- list containers
```
docker container ls -a
```

- remove/delete Docker images
```
docker rmi id#
docker images -f dangling=true

# delete all dangling images without any references
docker image rm -f $(docker images -f dangling=true -aq)

docker system prune
docker images purge
```

- stop all the services/containers
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

- inspect
```
docker container inspect $(docker container ls --last 1 --format
'{{.ID}}')
```
- When there is a change in the python code base, we obviously have to 
rebuild the docker image, isn't? Use following steps to do so:
```shell script
docker container ls
docker stop {id}
docker rm {id}
docker build ...
# for multiple shells for same container
docker exec -it <container> bash

```

- Docker image disk usage : `docker system df` 
  
- [Get the size of images befroe pull](https://stackoverflow.com/questions/33352901/get-the-size-of-a-docker-image-before-a-pull)

**Volumes**
 - [https://www.baeldung.com/ops/docker-volumes](https://www.baeldung.com/ops/docker-volumes)
- [https://stackoverflow.com/questions/23439126/how-to-mount-a-host-directory-in-a-docker-container](https://stackoverflow.com/questions/23439126/how-to-mount-a-host-directory-in-a-docker-container)
```
sudo apt-get install virtualbox-guest-x11
sudo mount -t vboxsf /opt/vlab/spark-streaming-playground/ /mnt/dockerfolder
```



**References**

- https://towardsdatascience.com/a-complete-guide-to-building-a-docker-image-serving-a-machine-learning-system-in-production-d8b5b0533bde
- [https://www.bogotobogo.com/DevOps/DevOps-Kubernetes-1-Running-Kubernetes-Locally-via-Minikube.php](https://www.bogotobogo.com/DevOps/DevOps-Kubernetes-1-Running-Kubernetes-Locally-via-Minikube.php)
- https://blog.adriel.co.nz/2018/01/25/change-docker-data-directory-in-debian-jessie/
- https://rominirani.com/docker-tutorial-series-part-7-data-volumes-93073a1b5b72
- https://medium.com/rahasak/kafka-and-zookeeper-with-docker-65cff2c2c34f
- https://github.com/sameersbn/docker-postgresql
- https://github.com/kibatic/docker-single-node-hadoop/
- https://github.com/bbonnin/docker-hadoop-3/blob/master/Dockerfile
- Permission Denied Error @ https://stackoverflow.com/questions/47854463/docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socke
- https://gist.github.com/nathzi1505/d2aab27ff93a3a9d82dada1336c45041