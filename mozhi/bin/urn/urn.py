# Import datasets here
from mozhi.dataset.ner.conll.hf_conll_2003 import HFConll2003Dataset
from mozhi.dataset.ner.conll.vf_conll_2003 import CoNLL2003DatasetV0
from mozhi.dataset.ner.sroie2019.hf_sroie_2019 import HFSREIO2019Dataset

# Add new model import here
from mozhi.model.pytorch.ner.bilstm_crf_torch import BiLSTMCRFTorch
from mozhi.model.pytorch.ner.lstm import LSTMTagger
from mozhi.model.tf.ner.bilstm import BiLSTMCRF

# Add new datasets to the list here
from mozhi.preprocessor.hf_tokenizer import HFTokenizer
from mozhi.preprocessor.conll_sentence import SentencePreprocessor


class URNLoader(object):
    """
    Uniform Resource Name Class Loader
    """
    def __init__(self) -> None:
        super().__init__()
        # Add new datasets to the list here
        datasets = [CoNLL2003DatasetV0, HFConll2003Dataset, HFSREIO2019Dataset]
        # Add new models to the list here, respectively
        torch_models = [LSTMTagger, BiLSTMCRFTorch]
        tf_models = [BiLSTMCRF]
        preprocessor = [SentencePreprocessor, HFTokenizer]

        # Auto create Dataset Name -> Dataset Object dictionary for all models
        self._dataset_obj_map = {d.NAME: d for d in datasets}
        # Create Model Name -> Model Object dictionary for all models
        self._pytorch_model_object_map = {m.NAME: m for m in torch_models}
        self._tf_model_object_map = {m.NAME: m for m in tf_models}
        self._preprocessor_model_object_map = {d.NAME: d for d in preprocessor}

    def load_model_class(self, name: str):
        if name in self._pytorch_model_object_map:
            return self._pytorch_model_object_map[name]
        elif name in self._tf_model_object_map:
            return self._tf_model_object_map[name]
        else:
            return NotImplementedError(f"Requested model: {name} is not available")

    def load_dataset_class(self, name: str):
        if name in self._dataset_obj_map:
            return self._dataset_obj_map[name]
        else:
            raise NotImplementedError(f"Requested dataset : {name} is not available")

    def load_preprocess_class(self, name: str):
        if name in self._preprocessor_model_object_map:
            return self._preprocessor_model_object_map[name]
        else:
            raise NotImplementedError(f"Requested preprocessor : {name} is not available")