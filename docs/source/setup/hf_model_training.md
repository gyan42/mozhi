# Hugging Face Transformers

## Preparing the model

- Train HF transfomer with custom dataset

```bash
cd /path/to/mozhi/
export PYTHONPATH=$(pwd)/:$PYTHONPATH
export ENV_FOR_VF=developement

python mozhi/bin/trainers/hf_trainer.py \
--dataset_name=HFConll2003Dataset \
--hf_pretrained_model_checkpoint=distilbert-base-uncased \
--hf_pretrained_tokenizer_checkpoint=distilbert-base-uncased \
--preprocessor_name=HFTokenizer \
--model_n_version=bertv1
```

- Package the trained model for Pytorch serving 

```bash
export SERIALIZED_MODEL_FILE=${HOME}/.mozhi/models/hf/bertv1/pytorch_model.bin

# Archive Torch models for serving
torch-model-archiver --force \
--model-name bertv1 \
--version 1.0 \
--serialized-file  $SERIALIZED_MODEL_FILE \
--handler mozhi/serve/torch/handler/hf_transformer_handler.py \
--extra-files ${HOME}/.mozhi/models/hf/bertv1/config.json,${HOME}/.mozhi/models/hf/bertv1/special_tokens_map.json,${HOME}/.mozhi/models/hf/bertv1/training_args.bin,${HOME}/.mozhi/models/hf/bertv1/tokenizer_config.json,${HOME}/.mozhi/models/hf/bertv1/vocab.txt \
--export-path ${HOME}/.mozhi/model_store/

#check new bertv1.mar file is created or not
ls ${HOME}/.mozhi/model_store/
```

## Testing

-  Test the PyTorch handler locally
```bash
unzip ${HOME}/.mozhi/model_store/bertv1.zip to -d ${HOME}/.mozhi/model_store/bertv1/
python mozhi/serve/torch/handler/hf_transformer_handler.py \
--unserialized_mar_dir ~/.mozhi/model_store/bertv1/ \
--sequence "Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very close to the Manhattan Bridge."
```

- Test PyTorch Serve on our custom docker image. Refer [TorchServe REST API](https://github.com/pytorch/serve/blob/master/docs/rest_api.md) for more details on APIs

```bash
docker run --rm -it \
--network host \
mozhi-api-cpu bash

# Command to run inside the docker
torchserve --start --model-store /home/model-server/model-store --models all --ts-config configs/torch_serve_config.properties --foreground
```

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
- Test the TorchServe REST API endpoint
```bash
python mozhi/bin/serve/test_api.py --url http://127.0.0.1:6543/predictions/bertv1
```