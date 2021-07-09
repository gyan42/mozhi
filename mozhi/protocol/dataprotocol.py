from dataclasses import dataclass
from typing import List, Dict
from dataclasses import asdict


def dataclass_to_dict(dataclass):
    return asdict(dataclass)

@dataclass(frozen=True)
class NERDatasetInfo:
    name: str
    words: List[str]
    tags: List[str]
    tot_num_words: int
    tot_num_tags: int
    max_sent_len: int


@dataclass(frozen=True)
class NERPreprocessorInfo:
    vocab_size: int
    tot_num_tags: int
    max_sent_len: int
    w2i: Dict[(str, int)]
    t2i: Dict[(str, int)]
    i2t: Dict[(int, str)]


@dataclass(frozen=True)
class NERModelInfo:
    name: str
    model_dir: str
    is_pytorch: bool
    is_tensorflow: bool
