# OCR

## Docker

`
export VERSION=0.7
`

- [Dockerfile](../../../ops/docker/ocr/Dockerfile)

- CPU Build
```
docker build -t mozhi-ocr-cpu:latest -f ops/docker/ocr/cpu/Dockerfile .
```
- GPU Build
```
docker build -t mozhi-ocr-gpu:latest -f ops/docker/ocr/gpu/Dockerfile .
```

- Run on local image
```
docker container  run --network host --gpus all -it --rm --name mozhi-ocr-gpu mozhi-ocr-gpu:latest

#bash for debugging
cd /path/to/mozhi/
docker container  run -p 8089:8089 -v $(pwd)/api:/api -v $(pwd)/data:/data --network host --gpus all -it --rm --name mozhi-ocr-gpu mozhi-ocr-gpu:latest bash
```

- Push to Dockerhub    
```
docker tag mozhi-ocr-gpu:latest mageswaran1989/mozhi-ocr-gpu:$VERSION
docker push mageswaran1989/mozhi-ocr-gpu:$VERSION

docker tag mozhi-ocr-gpu:latest mageswaran1989/mozhi-ocr-gpu:latest
docker push mageswaran1989/mozhi-ocr-gpu:latest

docker tag mozhi-ocr-cpu:latest mageswaran1989/mozhi-ocr-cpu:$VERSION
docker push mageswaran1989/mozhi-ocr-cpu:$VERSION

docker tag mozhi-ocr-cpu:latest mageswaran1989/mozhi-ocr-cpu:latest
docker push mageswaran1989/mozhi-ocr-cpu:latest
```

## Models
**Craft**
[https://drive.google.com/uc?id=1xcE9qpJXp4ofINwXWVhhQIh9S8Z7cuGj](https://drive.google.com/uc?id=1xcE9qpJXp4ofINwXWVhhQIh9S8Z7cuGj)
[https://drive.google.com/uc?id=1bupFXqT-VU6Jjeul13XP7yx2Sg5IHr4J](https://drive.google.com/uc?id=1bupFXqT-VU6Jjeul13XP7yx2Sg5IHr4J)

**[Calamari](../calamari.md)**