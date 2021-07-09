from abc import abstractmethod, ABC

from transformers import TFBertForTokenClassification, TFBertForSequenceClassification

class _ScikitCompat(ABC):
    """
    Interface layer for the Scikit and Keras compatibility.
    """

    @abstractmethod
    def transform(self, X):
        raise NotImplementedError()

    @abstractmethod
    def predict(self, X):
        raise NotImplementedError()


class Pipeline(object):
    def __init__(self, tokenizer, model):
        self._tokenizer = tokenizer
        self._model = model

    def __call__(self, *args, **kwargs):
        return self._model(self._tokenizer(*args, **kwargs))

