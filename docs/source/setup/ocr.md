
### OCR Image

```
docker build -t mozhi-ocr-gpu:latest -f ops/docker/ocr/Dockerfile .
docker container  run --network host --gpus all -it --rm --name mozhi-ocr-gpu mozhi-ocr-gpu:latest bash 
```
