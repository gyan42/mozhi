- Tensorflow

  ```
  cd /path/to/mozhi/
  export PYTHONPATH=$(pwd)/:$PYTHONPATH
  export ENV_FOR_VF=developement
  
  python mozhi/bin/trainers/tf_trainer.py \
  --dataset_name="CoNLL2003DatasetV0" \
  --preprocessor_name="NaiveSentencePreprocessor" \
  --model_name="BiLSTMCRF"
  ```
  
  Tensorboard: `tensorboard --logdir ${HOME}/.mozhi/logs/models/`