from typing import Union, List, Callable
import tensorflow as tf
from mozhi.preprocessor.ipreprocessor import IPreprocessor
from mozhi.protocol.dataprotocol import NERDatasetInfo, NERPreprocessorInfo, dataclass_to_dict
from mozhi.utils.pretty_print import print_error


class SentencePreprocessor(IPreprocessor):
    """
    Preprocessor for CoNLL like dataset
    """
    NAME = 'NaiveSentencePreprocessor'

    def __init__(self,
                 words: List[str],
                 tags: List[str],
                 max_sent_len: int,
                 embeddings: Callable[[str], Union[int, float]]=None,
                 **kwargs):
        """

        Args:
            words: list of words
            tags: list of tags
            max_len: Maximum length of sentence in the training dataset
        """
        IPreprocessor.__init__(self,
                               words=words,
                               tags=tags,
                               max_sent_len=max_sent_len,
                               embeddings=embeddings)

    @staticmethod
    def init_vf(dataset_info: NERDatasetInfo):
        kwargs = dataclass_to_dict(dataset_info)
        return SentencePreprocessor(**kwargs)

