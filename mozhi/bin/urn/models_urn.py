from mozhi.model.pytorch.ner.bilstm_crf_torch import BiLSTMCRFTorch
from mozhi.model.pytorch.ner.lstm import LSTMTagger
from mozhi.model.tf.ner.bilstm import BiLSTMCRF

# Add new models to the list here
torch_models = [LSTMTagger, BiLSTMCRFTorch]
tf_models = [BiLSTMCRF]


# Create Model Name -> Model Object dictionary for all models
PYTORCH_MODEL_OBJECT_MAP = {m.NAME: m for m in torch_models}

TF_MODEL_OBJECT_MAP = {m.NAME: m for m in tf_models}




