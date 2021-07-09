import os
from pathlib import Path
from typing import Dict, Union, List

import numpy as np

import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

from mozhi.model.tf.ner.crf import CRF
from mozhi.protocol.dataprotocol import NERPreprocessorInfo, dataclass_to_dict


# https://github.com/cswangjiawei/pytorch-NER
# https://pytorch.org/tutorials/beginner/nlp/advanced_tutorial.html

class BiLSTMCRF(tf.keras.Model):
    NAME = "BiLSTMCRF"
    def __init__(self,
                 vocab_size: int,
                 tot_num_tags: int,
                 max_sent_len: int,
                 word_embeddings_size=64,
                 checkpoint_dir=os.path.join(str(Path.home()), '.mozhi', 'models', 'ner'),
                 *args,
                 **kwargs):
        super(BiLSTMCRF, self).__init__()
        num_words = vocab_size
        num_tags = tot_num_tags
        sentence_max_length = max_sent_len

        self._word_embeddings_size = word_embeddings_size
        self._checkpoint_dir = os.path.expanduser(checkpoint_dir)
        self._file_name = "vf-bi-lstm-crf"
        self.model_file_path = self._checkpoint_dir + "/" + self._file_name

        # Embedding Layer
        self._embedding = tf.keras.layers.Embedding(input_dim=num_words,
                                                    output_dim=word_embeddings_size,
                                                    input_length=sentence_max_length)

        # BI-LSTM Layer
        self._bilstm = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units=word_embeddings_size,
                                                                          return_sequences=True,
                                                                          dropout=0.5,
                                                                          recurrent_dropout=0.5,
                                                                          kernel_initializer=tf.keras.initializers.HeNormal()))

        self._lstm = tf.keras.layers.LSTM(units=word_embeddings_size * 2,
                                          return_sequences=True,
                                          dropout=0.5,
                                          recurrent_dropout=0.5,
                                          kernel_initializer=tf.keras.initializers.HeNormal())

        # TimeDistributed Layer
        self._time_dist = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(num_tags,
                                                                                activation="relu"))

        self._crf = CRF(num_tags, sparse_target=True)

    @staticmethod
    def init_vf(preprocessor_data_info: NERPreprocessorInfo,
                word_embeddings_size=64,
                checkpoint_dir=os.path.join(str(Path.home()), '.mozhi', 'models', 'ner')):
        kwargs = dataclass_to_dict(preprocessor_data_info)
        kwargs.update({"word_embeddings_size":word_embeddings_size, "checkpoint_dir": checkpoint_dir})
        return BiLSTMCRF(**kwargs)

    def custom_preprocessing(self, raw_text: str) -> tf.string:
        lowercase = tf.strings.lower(raw_text)
        return lowercase

    def init_vectorize_layer(self, text_dataset: np.ndarray) -> TextVectorization:
        self._text_vectorizer = TextVectorization(max_tokens=self.max_features,
                                                  standardize=self.custom_preprocessing,
                                                  output_mode='int',
                                                  output_sequence_length=self.max_len)
        self._text_vectorizer.adapt(text_dataset)


    def call(self, x):
        x = self._text_vectorizer(x)
        x = self._embedding(x)
        x = self._bilstm(x)
        x = self._lstm(x)
        x = self._time_dist(x)
        logits = self._crf(x)
        return logits

    @property
    def optimizer(self):
        return tf.keras.optimizers.Adam(learning_rate=0.0005, beta_1=0.9, beta_2=0.999)

    @property
    def loss(self):
        return self._crf.loss

    @tf.function(input_signature=[tf.TensorSpec(shape=(1,), dtype=tf.string)])
    def prediction(self, review: str) -> Dict[str, Union[str, List[float]]]:
        return {'prediction': self.model(review),
                'description': 'prediction ranges from 0 (negative) to 1 (positive)'}
