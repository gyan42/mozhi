# Pytorch 

**Build custom Deep Learning Models**

```
cd /path/to/mozhi/
export PYTHONPATH=$(pwd)/:$PYTHONPATH
export ENV_FOR_VF=developement

python mozhi/bin/trainers/pytorch_trainer.py \
--experiment_name="conll2003" \
--dataset_name="CoNLL2003DatasetV0" \
--preprocessor_name="NaiveSentencePreprocessor" \
--model_name="BiLSTMCRFTorch"
```

Tensorboard: `tensorbloard --logdir=${HOME}/.mozhi/logs/pytorch/{MODEL_NAME}`


**Inference using custom build models**

```
cd /path/to/mozhi/
export PYTHONPATH=$(pwd)/:$PYTHONPATH
export ENV_FOR_VF=developement

#Note: Change model_chk_pth path accordingly

python mozhi/bin/estimators/pytorch_infer.py \
--experiment_name="conll2003" \
--preprocessor_name="NaiveSentencePreprocessor" \
--model_name="BiLSTMCRFTorch" \
--preprocessor_dir="${HOME}/.mozhi/preprocessor/conll2003/" \
--model_chk_pth="${HOME}/.mozhi/models/pytorch/conll2003/bilstmcrftorch/bilstmcrftorch-epoch=01-val_loss=296.76.ckpt" \
--sentence="LONDON 1996-08-22 The following floating-rate issue was announced by lead manager Lehman Brothers International ."

# Expected output: B-LOC O O O O O O O O O O B-ORG I-ORG I-ORG O
```

**Serving custom build models** (WIP)

```
mkdir -p ${HOME}/.mozhi/model_store/

export SERIALIZED_MODEL_FILE=${HOME}/.mozhi/models/pytorch/conll2003/bilstmcrftorch/bilstmcrftorch.pt
# or
export SERIALIZED_MODEL_FILE=${HOME}/.mozhi/models/pytorch/conll2003/bilstmcrftorch/bilstmcrftorch-epoch=00-val_loss=0.57.ckpt

# Archive Torch models for serving
torch-model-archiver --force\
--model-name bilstmcrf \
--version 1.0 \
--model-file mozhi/model/pytorch/ner/bilstm_crf_torch.py \
--serialized-file  $SERIALIZED_MODEL_FILE\
--handler mozhi/serve/torch/handler/ner_handler.py \
--extra-files ${HOME}/.mozhi/preprocessor/conll2003/NaiveSentencePreprocessor \
--export-path ${HOME}/.mozhi/model_store/ \

# Manually start torchserve
torchserve \
 --start \
 --ts-config configs/torch_serve_config.properties \
 --model-store ${HOME}/.mozhi/model_store/ \
 --models bilstmcrf.mar \
 --foreground

# Run with docker
docker run --rm -it \
-p 6543:6543 -p 6544:6544 -p 6545:6545 -p 7070:7070 -p 7071:7071 \
-p 8080:8080 -p 8081:8081 -p 8082:8082 \
-v ${HOME}/.mozhi/model_store:/home/model-server/model-store \
-v $(pwd)/mozhi/:/home/model-server/mozhi \
mozhi-api-cpu bash

# Command to run inside the docker
torchserve --start --model-store /home/model-server/model-store --models bilstmcrf.mar --ts-config configs/torch_serve_config.properties --foreground

# Test code to run from host
python mozhi/bin/serve/test_api.py

# stop torchserve
torchserve --stop
```