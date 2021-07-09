# Load and Prepare Data for UI

- [MinIO](https://min.io/) is used as self hosted object store that is similar to S3.

By default, the MinIO server doesn't have any user data, please follow steps below to load the
demo data to MinIO server.

**Important**: Create alias for MinIO server, refer [here](minio.md)
```#create alias to MinIO server, if not done already
mcli alias set myminio http://192.168.0.142:9000 admin password
```

- [Postgresql](Postgres.md) is used as DB store.


1. Text Data : ConLL 2003 dataset is loaded into Possgresql Database server to demonstrate the tagger 
```bash
cd /path/to/mozhi/

export PYTHONPATH=$PYTHONPATH:$(pwd)/mozhi/

# upload ConLL 2003 annotated data to Database
python mozhi/bin/db/upload.py \
--host localhost \
--port 4321 \
--db_name mozhidb \
--user mozhi \
--password mozhi \
--experiment_name conll2003 \
--is_delete true \
--is_conll true \
--dir_root data/ner/conll/2003/
```



2. Images

```bash
#create bucket and copy data
mcli mb myminio/mozhi/
mcli policy set download myminio/mozhi/
# copy receipts
mcli mb myminio/mozhi/data/receipts/
mcli cp data/receipts/* myminio/mozhi/data/receipts/

mcli ls myminio/mozhi/data/receipts/
```

3. Model files, to build model refer [here](hf_model_training.md)

```bash
# create bucket folders
mcli mb myminio/mozhi/model-store/

# copy from local build model, if trained
mcli cp ${HOME}/.mozhi/model_store/bertv1.mar myminio/mozhi/model-store/

# or use prebuild image from Git repo (preferred for demo purpose)
cd /path/to/mozhi/data
git clone https://github.com/gyan42/model-store
mcli cp model-store/hugging_face/bertv1.mar myminio/mozhi/model-store/
# important make the file downloadable
mcli policy set public myminio/mozhi/model-store/bertv1.mar
```

4. Register the model on Torch Serve 

```bash
# Register the model 
curl -X POST  "http://localhost:6544/models?initial_workers=1&synchronous=true&url=http://192.168.0.142:9000/mozhi/model-store/bertv1.mar"
# Increase the workers
curl -v -X PUT "http://localhost:6544/models/bertv1?min_worker=3&synchronous=true"
# Unregister the model
curl -X DELETE http://localhost:6544/models/bertv1/1.0
#list down the models
curl "http://localhost:6544/models"
```