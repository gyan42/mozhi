import shutil

import pytest

from mozhi.dataset.ner.conll.vf_conll_2003 import CoNLL2003DatasetV0

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


def test_train_sentences(vf_conll_2003: CoNLL2003DatasetV0):
    assert 12855 == len(vf_conll_2003.train_tuple_pairs)


def test_valid_sentences(vf_conll_2003: CoNLL2003DatasetV0):
    assert 3002 == len(vf_conll_2003.val_tuple_pairs)


def test_test_sentences(vf_conll_2003: CoNLL2003DatasetV0):
    assert 3181 == len(vf_conll_2003.test_tuple_pairs)


def test_dataset_info(vf_conll_2003: CoNLL2003DatasetV0):
    dataset_info = vf_conll_2003.get_dataset_info()
    assert dataset_info.tot_num_tags == 9
    assert dataset_info.max_sent_len == 113
    assert dataset_info.tot_num_words == 23623
    assert dataset_info.name == "conll2003"