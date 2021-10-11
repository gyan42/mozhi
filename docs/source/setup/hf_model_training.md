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
--model_n_version=conll2003v1


python mozhi/bin/trainers/hf_trainer.py \
--dataset_name=HFSREIO2019Dataset \
--hf_pretrained_model_checkpoint=distilbert-base-uncased \
--hf_pretrained_tokenizer_checkpoint=distilbert-base-uncased \
--preprocessor_name=HFTokenizer \
--model_n_version=sroie2019v1
```

- Package the trained model for Pytorch serving 

```bash
export SERIALIZED_MODEL_FILE=${HOME}/.mozhi/models/hf/conll2003v1/pytorch_model.bin

mkdir -p  ${HOME}/.mozhi/model-store/

# Archive Torch models for serving
torch-model-archiver --force \
--model-name conll2003v1 \
--version 1.0 \
--serialized-file  $SERIALIZED_MODEL_FILE \
--handler mozhi/serve/torch/handler/hf_transformer_handler.py \
--extra-files ${HOME}/.mozhi/models/hf/conll2003v1/config.json,${HOME}/.mozhi/models/hf/conll2003v1/special_tokens_map.json,${HOME}/.mozhi/models/hf/conll2003v1/training_args.bin,${HOME}/.mozhi/models/hf/conll2003v1/tokenizer_config.json,${HOME}/.mozhi/models/hf/conll2003v1/vocab.txt \
--export-path ${HOME}/.mozhi/model-store/

#check new sroie2019v1.mar file is created or not
ls ${HOME}/.mozhi/model-store/

export SERIALIZED_MODEL_FILE=${HOME}/.mozhi/models/hf/sroie2019v1/pytorch_model.bin

# Archive Torch models for serving
torch-model-archiver --force \
--model-name sroie2019v1 \
--version 1.0 \
--serialized-file  $SERIALIZED_MODEL_FILE \
--handler mozhi/serve/torch/handler/hf_transformer_handler.py \
--extra-files ${HOME}/.mozhi/models/hf/sroie2019v1/config.json,${HOME}/.mozhi/models/hf/sroie2019v1/special_tokens_map.json,${HOME}/.mozhi/models/hf/sroie2019v1/training_args.bin,${HOME}/.mozhi/models/hf/sroie2019v1/tokenizer_config.json,${HOME}/.mozhi/models/hf/sroie2019v1/vocab.txt \
--export-path ${HOME}/.mozhi/model-store/

#check new conll2003v1.mar file is created or not
ls ${HOME}/.mozhi/model-store/
```

## Testing

-  Test the PyTorch handler locally
```bash
unzip ${HOME}/.mozhi/model-store/conll2003v1.zip -d ${HOME}/.mozhi/model-store/conll2003v1/

python mozhi/serve/torch/handler/hf_transformer_handler.py \
--unserialized_mar_dir ~/.mozhi/model-store/conll2003v1/ \
--sequence "Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very close to the Manhattan Bridge."


unzip ${HOME}/.mozhi/model-store/sroie2019v1.mar -d ${HOME}/.mozhi/model-store/sroie2019v1/

python mozhi/serve/torch/handler/hf_transformer_handler.py \
--unserialized_mar_dir ~/.mozhi/model-store/sroie2019v1/ \
--sequence "OCEAN IC PACKAGING ENTERPRISE GST NO: 000945983488 41-1J PETALING.57000 KUALA LUMPUR H/P:012-3163818 FAX:0390542829 TAX INVOICE 12:45 #027553 27/06/2018 01LAI 000000 RM152.00 4X 38.00 OTHERS SUBTOTAL RM152.00 GST TAXABLE RM152.00 GST 0% RM0.00 ITEMS 40 RM152.00 CASH"
```

- Test PyTorch Serve on our custom docker image. Refer [TorchServe REST API](https://github.com/pytorch/serve/blob/master/docs/rest_api.md) for more details on APIs

```bash
export MODEL_DATA=/opt/vlab/gyan42/model-store/huggingface

docker run --rm -it \
-v $MODEL_DATA:/home/model-server/model-store \
--network host \
mozhi-api-cpu bash


docker run --rm -it \
-v $MODEL_DATA:/home/model-server/model-store \
-p 6543:6543 -p 6544:6544 -p 6545:6545 \
mozhi-api-cpu bash

# Command to run inside the docker
torchserve --start --model-store /home/model-server/model-store --models all --ts-config configs/torch_serve_config.properties --foreground
```

```bash
# Register the model 
curl -X POST  "http://localhost:6544/models?initial_workers=1&synchronous=true&url=http://192.168.0.142:9000/mozhi/model-store/conll2003v1.mar"
# Increase the workers
curl -v -X PUT "http://localhost:6544/models/conll2003v1?min_worker=3&synchronous=true"
# Unregister the model
curl -X DELETE http://localhost:6544/models/conll2003v1/1.0
#list down the models
curl "http://localhost:6544/models"
```
- Test the TorchServe REST API endpoint
```bash
python mozhi/bin/serve/test_api.py --url http://127.0.0.1:6543/predictions/conll2003v1
```