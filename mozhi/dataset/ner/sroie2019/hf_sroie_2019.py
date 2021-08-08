"""
CoNLL 2003 Dataset

Refs:
    https://github.com/ebanalyse/NERDA/blob/main/src/NERDA/datasets.py
    https://huggingface.co/datasets/conll2003
"""

import os
from pathlib import Path
from datasets import load_dataset, ClassLabel, DownloadConfig
from mozhi.dataset.idataset import IDataset
from mozhi.dataset.ner.sroie2019.sroie2019 import SROIE2019


class HFSREIO2019Dataset(IDataset):
    """
    """
    NAME = "HFSREIO2019Dataset"
    def __init__(self):
        config = DownloadConfig(cache_dir=os.path.join(str(Path.home()), '.mozhi'))
        self._dataset = SROIE2019()
        self._dataset.download_and_prepare(download_config=config)
        self._dataset = self._dataset.as_dataset()

    @property
    def datasets(self):
        return self._dataset

    @property
    def labels(self) -> ClassLabel:
        return self._dataset['train'].features['ner_tags'].feature.names

    @property
    def id2label(self):
        return dict(list(enumerate(self.labels)))

    @property
    def label2id(self):
        return {v: k for k, v in self.id2label.items()}

    def train(self):
        return self._dataset['train']

    def test(self):
        return self._dataset["test"]

    def validation(self):
        return self._dataset["validation"]


if __name__ == "__main__":
    # train_data = get_conll_data("train")
    # print(train_data)
    train_data = HFSREIO2019Dataset()