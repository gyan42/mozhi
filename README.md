# Mozhi - A full stack for Named Entity Recognition tasks

![](docs/drawio/mozhi_software_stack.png)


## Contents

- [Features](features)
- [Developer Machine Setup](docs/source/setup/dev_machine.md)
- [How to run?](how)
- [Testing](testing)
- [Documentation](docs)

## [Features](#features)

- Web based NER Tagger using [Vue](vue.js)
  - Supports browser based tagging for text, csv, and parquet file formats
  - Persistent data support with PostgreSql database, along with build in tools to upload data
  - In-build support to tag images from object store
  - Comes with NER playground to load aviable models and test it
- Back-end engine using [FastAPI](https://fastapi.tiangolo.com/)
- Model serving using
  - Tensorflow serving
  - Pytorch serve
- Deep Learning Models
  - Dataset APIs
  - Well defined data preprocessor's
  - Minimal integration efforts for existing models
  - Support for developing custom Pytorch and Tensorflow models
  - Fully configurable training scripts


![](docs/images/mozhi_db_annotator.png)
![](docs/images/mozhi_image_annotator.png)
![](docs/images/mozhi_ner_playground.png)


## [How to run?](how)

- **Configs used are placed [here](configs)**
- **Build and run Docker containers:** 

```
minikube start
minikube addons enable ingress
kubectl apply -f ops/k8s/services/
echo "$(kubectl get ingress | grep mozhi-api-ingress | cut -d' ' -f10) mozhi.ai"

# copy above line and add at top 
sudo vi /etc/hosts 
```

[Mozhi UI](mozhi.ai)

- **Training Models** (GPU is a must! Skip this part if you don't have a GPU and use prebuild models)
  - **[Hugging Face Transformers Models](docs/source/setup/hf_model_training.md)**
  - **[Pytorch Models](docs/source/setup/pt_model_training.md)** (Work In Progress)
  - **[Tensorflow Models](docs/source/setup/tf_model_training.md)** (Work In Progress)

- Follow the steps **[here to load and prepare the data for UI](docs/source/setup/prepare_data.md)** that are been used by the demo.

- Reference demo links
  - [Mozhi UI](https://localhost:8080)
  - [Mozhi API](https://localhost:8088)
  - [MinIO](http://localhost:9000)
      - user: `admin`
      - password: `password`
  - [PGAdmin](http://localhost:5050/)
      - `user: admin@admin.com  pass: root`
      - Create a new connection `user: Mozhi pass Mozhi`
      - Test from postgresql Command line
        ```
          psql --host=localhost --dbname=Mozhidb --username=Mozhi
        ```

## [Testing](#testing)

pytest flags:
- `s` #prints all logs to the terminal
- `rP` #shows the captured output of passed tests.
- `rx` #shows the captured output of failed tests (default behaviour).

```
export PYTHONPATH=$PYTHONPATH:$(pwd)/Mozhi/
export PYTHONPATH=$PYTHONPATH:$(pwd)/tests/

pytest -s 
```

## [Documentation](#docs)

**Build Documents**
```
export PYTHONPATH=$(pwd):$PYTHONPATH
cd docs
pip install -r requirements.txt
make Mozhi
```

## Misc

- In case if Postresql port is already in use: `systemctl stop postgresql`
- Port errors
```bash
# command to check port usage
export PORTNO=8080
sudo lsof -i -P -n | grep LISTEN | grep $PORTNO

#command to kill all running docker instances
docker kill $(docker ps -q) 
```
