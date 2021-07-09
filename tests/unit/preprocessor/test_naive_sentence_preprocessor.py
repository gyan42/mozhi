import pytest

from mozhi.dataset.ner.conll.vf_conll_2003 import CoNLL2003DatasetV0
from mozhi.preprocessor.conll_sentence import SentencePreprocessor

@pytest.fixture(scope="session")
def vf_conll_2003():
    obj = CoNLL2003DatasetV0(train_file_path="~/.mozhi/data/ner/conll/2003/train.txt",
                             val_file_path="~/.mozhi/data/ner/conll/2003/valid.txt",
                             test_file_path="~/.mozhi/data/ner/conll/2003/test.txt",
                             unknown_word='unk',
                             text_col=0,
                             ner_tag_col=3,
                             cache_dir=None,
                             delete_cache=True)
    return obj

@pytest.fixture(scope="session")
def naive_sentence_preprocessor(vf_conll_2003):
    obj = SentencePreprocessor(dataset_info=vf_conll_2003.get_dataset_info())
    return obj


def test_get_preprocessor_info(naive_sentence_preprocessor: SentencePreprocessor):
    preprocessor_info = naive_sentence_preprocessor.get_preprocessor_info()
    assert preprocessor_info.tot_num_tags == 9 + 2
    assert preprocessor_info.max_sent_len == 113 + 2
    assert preprocessor_info.vocab_size == 23623 + 2

