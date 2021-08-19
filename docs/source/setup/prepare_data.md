# Load and Prepare Demo Data for UI

- [MinIO](https://min.io/) is used as self hosted object store that is similar to S3.

By default, the MinIO server doesn't have any user data, please follow steps below to load the
demo data to MinIO server.

**Important**: Create alias for MinIO server, refer [here](minio.md)
```#create alias to MinIO server, if not done already
mcli alias set mozhiminio http://localhost:9000 mozhi mozhi123
```

- [Postgresql](postgres.md) is used as DB store.

------------------------------------------------------------------------------------------------------------------------

1. Text Data : ConLL 2003 dataset is loaded into Postgresql Database server to experience the tagger 
```bash
cd /path/to/mozhi/

export PYTHONPATH=$PYTHONPATH:$(pwd)/mozhi/

# upload ConLL 2003 annotated data to Database
python mozhi/bin/db/upload.py \
--host localhost \
--port 5432 \
--db_name mozhidb \
--user mozhi \
--password mozhi \
--experiment_name conll2003 \
--is_delete true \
--is_conll true \
--dir_root data/conll/2003/
```

2. Images

```bash
#create bucket and copy data
mcli mb mozhiminio/mozhi/
mcli policy set download mozhiminio/mozhi/
# copy receipts
mcli mb mozhiminio/mozhi/data/receipts/
mcli cp data/receipts/* mozhiminio/mozhi/data/receipts/

mcli ls mozhiminio/mozhi/data/receipts/
```

3. Model files, to build model refer [here](hf_model_training.md)

```bash
# create bucket folders
mcli mb mozhiminio/mozhi/model-store/

# copy from local build model, if trained
mcli cp ${HOME}/.mozhi/model-store/* mozhiminio/mozhi/model-store/

# or use prebuild image from Git repo (preferred for demo purpose)
cd /path/to/mozhi/data
git clone https://github.com/gyan42/model-store
cd data/model-store/
mcli cp huggingface/* mozhiminio/mozhi/model-store/
mcli ls mozhiminio/mozhi/model-store/
# important make the file downloadable
mcli policy set download mozhiminio/mozhi/model-store/conll2003v1.mar
mcli policy set download mozhiminio/mozhi/model-store/sroie2019v1.mar
```

4. Register the model on Torch Serve 

```bash

kubectl port-forward service/mozhi-api-torchserve-svc 6543:6543 6544:6544 6545:6545  -n mozhi
kubectl port-forward service/minio 9000:80 -n mozhi

# Register the model 
curl -X POST  "http://localhost:6544/models?initial_workers=1&synchronous=true&url=http://localhost:9000/mozhi/model-store/conll2003v1.mar"

               http://localhost:6544/models?initial_workers=1&synchronous=true&url=http://localhost:9000/mozhi/model-store/conll2003v1.mar

curl -X POST  "http://localhost:6544/models?initial_workers=1&synchronous=true&url=http://minio:80/mozhi/model-store/sroie2019v1.mar"
curl -X POST  "http://localhost:6544/models?initial_workers=1&synchronous=true&url=http://minio:80/mozhi/model-store/conll2003v1.mar"


# Increase the workers
curl -v -X PUT "http://localhost:6544/models/bertv1?min_worker=3&synchronous=true"
# Unregister the model
curl -X DELETE http://localhost:6544/models/bertv1/1.0
#list down the models
curl "http://localhost:6544/models"
```