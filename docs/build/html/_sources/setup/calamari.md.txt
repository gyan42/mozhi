# [Calamari](https://github.com/Calamari-OCR/calamari_models/)

## Dataset: 

Task 1 from [https://rrc.cvc.uab.es/?ch=13](https://rrc.cvc.uab.es/?ch=13)

For receipt OCR task, each image in the dataset is annotated with text bounding boxes (bbox)
and the transcript of each text bbox. Locations are annotated as rectangles with four vertices,
which are in clockwise order starting from the top. Annotations for an image are stored in a text
file with the same file name. The annotation format is similar to that of ICDAR2015 dataset,
which is shown below:

    x1_1, y1_1,x2_1,y2_1,x3_1,y3_1,x4_1,y4_1, transcript_1
    x1_2,y1_2,x2_2,y2_2,x3_2,y3_2,x4_2,y4_2, transcript_2
    x1_3,y1_3,x2_3,y2_3,x3_3,y3_3,x4_3,y4_3, transcript_3



## Docker Image

```
cd /path/to/mozhi/
docker build -t mozhi-ocr-gpu:latest -f ops/docker/ocr/Dockerfile .

docker container  \
run --network host \
--gpus all -it \
--rm --name mozhi-ocr-gpu \
-v $(pwd)/data/SROIE2019/:/data/ \
mozhi-ocr-gpu:latest bash 
```

Prepare data on Machine:

```
cd /path/to/mozhi/
export PYTHONPATH=$PYTHONPATH:$(pwd)/mozhi/
python mozhi/ocr/text_cropping/cropping.py --input_dir=data/SROIE2019/0325updated.task1train\(626p\)/ \
--file_ext=.jpg \
--out_dir=data/SROIE2019/cropped/ \
--num_threads=8
```

Calamari Training on Docker:

```
ls /data/0325updated.task1train\(626p\)/

calamari-train \
--device.gpus 0 \
--trainer.gen SplitTrain \
--trainer.gen.validation_split_ratio=0.2  \
--trainer.output_dir /data/model-output/ \
--trainer.epochs 25 \
--early_stopping.frequency=1 \
--early_stopping.n_to_go=3 \
--train.images /data/cropped/*.jpg
```
