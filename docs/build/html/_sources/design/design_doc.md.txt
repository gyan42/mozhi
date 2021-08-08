# Mozhi Design Documentation

This doc contains the design consideration and nitty-gritty that new developer needs to know before playing around the 
Mozhi tools.

## Deep Learning Models

Mozhi comes with three backend Deep Learning frameworks namely, `PyTorch`, `Tensorflow` and `HuggingFace`. All these 
three have their own API interfaces for datasets (preprocessing/loading/postprocessing), training and serving. Mozhi 
has a thin wrapper around these well established APIs, enabling to bring in existing datasets and models with minimal 
efforts and take advantage of end to end NER tools packaged with Mozhi

- **Config Management**
    - [Dynaconf](https://github.com/rochacbruno/dynaconf) is used for all configurations.
- **Datasets**
    - Inherit from IDataset class
    - Add entry to dataset urn
    - Add entry to datasets.toml
- **Models**
- **Model Serve**

## Database 
Table Schema
- Dataset

## UI - Vue3
- Environment

## API - FastAPI
- 
