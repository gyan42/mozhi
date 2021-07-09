"""
CoNLL 2003 Dataset

Refs:
    https://github.com/ebanalyse/NERDA/blob/main/src/NERDA/datasets.py
    https://huggingface.co/datasets/conll2003
"""

import os
from pathlib import Path
from datasets import load_dataset, ClassLabel
from mozhi.dataset.idataset import IDataset

class HFConll2003Dataset(IDataset):
    """
    """
    NAME = "HFConll2003Dataset"
    def __init__(self):
        self._dataset = load_dataset("conll2003", cache_dir=os.path.join(str(Path.home()), '.mozhi'))
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
    train_data = Conll2003Dataset()