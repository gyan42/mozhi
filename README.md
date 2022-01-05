# Mozhi - A full stack for Named Entity Recognition tasks

![](docs/drawio/mozhi_software_stack.png)


## Contents

- [Features](features)
- [Developer Guide](docs/source/setup/home.md)
- [How to run?](how)
- [Testing](tests/README.md)
- [Documentation](docs/README.md)

## [Features](#features)

- Web based NER Tagger using [Vue](vue.js)
  - Supports browser based tagging for text, csv, and parquet file formats
  - Persistent data support with PostgreSql database, along with build in tools to upload data
  - In-build support to tag images from object store
  - Comes with NER playground to load aviable models and test it
- Back-end API engine using [FastAPI](https://fastapi.tiangolo.com/)
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


## [How to run the demo?](how)

- [Set up local Kubernets cluster using Minikube](docs/source/setup/on_minikune.md)
  
- Training Models (GPU is a must! Skip this part if you don't have a GPU and use prebuild models)
  - [Hugging Face Transformers Models](docs/source/setup/hf_model_training.md)
  - [Pytorch Models](docs/source/setup/pt_model_training.md) (Work In Progress)
  - [Tensorflow Models](docs/source/setup/tf_model_training.md) (Work In Progress)
  
- Load demo data by following the steps [here](docs/source/setup/prepare_data.md)
  
- Demo links
  - [Mozhi UI](mozhi.ai)
  - [Mozhi API](https://localhost:8088)
  - [MinIO](http://localhost:9000)
      - user: `mozhi`
      - password: `mozhi123`

