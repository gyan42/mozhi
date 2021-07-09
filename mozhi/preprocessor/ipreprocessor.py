from abc import ABC
from typing import Union, List, Callable
from future.utils import iteritems
import tensorflow as tf
from torch.utils.data import DataLoader, TensorDataset

from mozhi.protocol.dataprotocol import NERDatasetInfo, NERPreprocessorInfo
from mozhi.utils.pickle_me import PickleMe
from mozhi.utils.pretty_print import print_info

# TODO https://gist.github.com/Mageswaran1989/70fd26af52ca4afb86e611f84ac83e97#file-text_preprocessing-ipynb
class IPreprocessor(ABC, PickleMe):
    def __init__(self,
                 words: List[str],
                 tags: List[str],
                 max_sent_len: int,
                 embeddings: Callable[[str], Union[int, float]]=None):
        self._pad_word = 'pad'
        self._unknown_word = "unk"
        self._pad_tag = '<pad>'
        self._unknown_tag = '<unk>'
        self._start_tag = "<start>"
        self._stop_tag = "<stop>"

        self._words = [self._unknown_word, self._pad_word] + words
        self._tags = [self._unknown_tag, self._pad_tag, self._start_tag, self._stop_tag] + tags

        self.num_tags = len(self._tags)  # dataset_info.tot_num_tags + 2
        self.num_words = len(self._words) # dataset_info.tot_num_words + 2
        self.max_len = max_sent_len #+ 2
        self._word2idx = {w: i for i, w in enumerate(self._words)}
        self._tag2idx = {t: i for i, t in enumerate(self._tags)}
        self._idx2tag = {v: k for k, v in iteritems(self._tag2idx)}

    def id2label(self, id):
        return self._idx2tag.get(id, 'O')

    def ids2labels(self, ids: List[int]):
        return [self.id2label(id) for id in ids]

    def sentences_to_data(self, sentence_tuples):
        """
        Converts the sentence + tag tuples into integer IDs for trinaing
        Args:
            sentence_tuples: [[(word1, tag1), (word2, tag2), ...],[...], ...]

        Returns:
            X :[], y: []
        """
        X = [[self._word2idx.get(w[0], self._word2idx[self._unknown_word]) for w in s] for s in sentence_tuples]
        X = tf.keras.preprocessing.sequence.pad_sequences(maxlen=self.max_len,
                                                          sequences=X,
                                                          padding="post",
                                                          dtype="long",
                                                          value=self._word2idx[self._pad_word])

        y = [[self._tag2idx.get(w[1], self._tag2idx[self._unknown_tag]) for w in s] for s in sentence_tuples]
        y = tf.keras.preprocessing.sequence.pad_sequences(maxlen=self.max_len,
                                                          sequences=y,
                                                          padding="post",
                                                          dtype="long",
                                                          value=self._tag2idx[self._pad_tag])
        return X, y

    def get_preprocessor_info(self) -> NERPreprocessorInfo:
        return NERPreprocessorInfo(max_sent_len=self.max_len,
                                   vocab_size=self.num_words,
                                   tot_num_tags=self.num_tags,
                                   w2i=self._word2idx,
                                   t2i=self._tag2idx,
                                   i2t=self._idx2tag)

    def get_tf_data_iterator(self, sentences):
        X, y = self.sentences_to_data(sentences)
        y = [tf.keras.utils.to_categorical(i, num_classes=self.num_tags) for i in y]
        return tf.data.Dataset.from_tensor_slices((X, y))

    def get_iterator(self, sentences):
        for s in sentences:
            yield s

    def get_torch_dataloader(self,
                             sentences,
                             batch_size=32,
                             num_workers=4,
                             shuffle=True):
        import torch
        X, y = self.sentences_to_data(sentences)
        data = TensorDataset(torch.tensor(X), torch.tensor(y))
        ret = DataLoader(data,
                         batch_size=batch_size,
                         num_workers=num_workers,
                         shuffle=shuffle)
        return ret

    def tokenize(self, sentence):
        if type(sentence) == bytes:
            sentence = sentence.decode('utf-8')
        print_info(f"Tokenizing {sentence}")
        tokens = sentence.split(" ")
        X = [[self._word2idx.get(w[0], self._word2idx[self._unknown_word]) for w in tokens]]
        X = tf.keras.preprocessing.sequence.pad_sequences(maxlen=self.max_len,
                                                          sequences=X,
                                                          padding="post",
                                                          dtype="long",
                                                          value=self._word2idx[self._pad_word])
        return X
