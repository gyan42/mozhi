# Setting up Developer Machine

## Installations
### 1. Ubuntu System Setup

[Cuda 11.1 Ubuntu 20.4](https://developer.nvidia.com/cuda-11.1.0-download-archive?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=2004&target_type=deblocal)   
[Java 11](https://linuxize.com/post/install-java-on-ubuntu-20-04/)   
[NVidia GPU Setup](nvidia.md)

```
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
sudo apt-get install postgresql postgresql-contrib
sudo apt install libpq-dev
sudo apt install git-lfs

#Torch with Cuda 11.1
conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c conda-forge
or 
pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
```

### 2. Python Environment

```
export VENV_DIR=/opt/envs/vf
conda create --prefix $VENV_DIR python=3.8
conda activate /opt/envs/vf

pip install -r requirements.txt
python -m spacy download en_core_web_md
```

### 3. [Postgresql](postgres.md)

### 4. [Vue 3 Js](https://v3.vuejs.org/guide/installation.html#download-and-self-host)

```
sudo apt install npm # or similar one based on your OS
yarn global add @vue/cli
npm i -g @vue/cli-service
npm install vue@next
```

### 5. Containers

Add following to your bash for cached builds.
```
export DOCKER_BUILDKIT=1
```

- [Docker Images](docker.md)
- [Kubernetes](kubernetes.md)

### 6. [MinIO](../setup/minio.md)/S3

```
#start MinIO server
MINIO_ROOT_USER=admin MINIO_ROOT_PASSWORD=password minio server /opt/minio/data/
mc alias set myminio http://192.168.0.142:9000 admin password
```


## Folder Structure

```
mozhi/
    docs/
    api/
       ... # Backend code using FastAPI
    ui/
       ... # Frontend code using Vue3
    mozhi/
       ... # mozhi DL framework source code 
```

