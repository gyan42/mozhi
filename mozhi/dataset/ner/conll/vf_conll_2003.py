import os
import pathlib
import pickle
from pathlib import Path
import shutil
import pandas as pd
from tqdm import tqdm
from mozhi.protocol.dataprotocol import NERDatasetInfo


class CoNLLLoader(object):
    def __init__(self,
                 unknown_word,
                 text_col=0,
                 ner_tag_col=3):
        self._unknown_word = unknown_word
        self._text_col = text_col
        self._ner_tag_col = ner_tag_col

    @ staticmethod
    def split_text_label(filename, sentence_len=2):
        '''
        Reads a file named filename, extracts the text and the labels and stores
        them in an array.

        returns
        [
        [['EU', 'B-ORG'], ['rejects', 'O'], ['German', 'B-MISC'], ['call', 'O'], ['to', 'O'], ['boycott', 'O'], ['British', 'B-MISC'], ['lamb', 'O'], ['.', 'O']],
         ]

        '''
        f = open(os.path.expanduser((filename)))
        split_labeled_text = []
        sentence = []
        for line in tqdm(f):
            if len(line) == 0 or line.startswith('-DOCSTART') or line[0] == "\n":
                if len(sentence) > sentence_len:
                    split_labeled_text.append(sentence)
                    sentence = []
                continue
            splits = line.split(' ')
            sentence.append([splits[0], splits[-1].rstrip("\n")])
        if len(sentence) > sentence_len:
            split_labeled_text.append(sentence)
            sentence = []
        return split_labeled_text

    def load(self, in_file_path, pickled_file_path):
        '''
        Reads a file named filename, extracts the text and the labels and stores
        them in an array.

        returns
        [
        [['EU', 'B-ORG'], ['rejects', 'O'], ['German', 'B-MISC'], ['call', 'O'], ['to', 'O'], ['boycott', 'O'], ['British', 'B-MISC'], ['lamb', 'O'], ['.', 'O']],
         ]

        '''
        parent_dir = pathlib.Path(pickled_file_path).parent
        os.makedirs(parent_dir, exist_ok=True)
        if not os.path.exists(pickled_file_path):
            sentences = CoNLLLoader.split_text_label(in_file_path)
            with open(pickled_file_path, "wb") as f:
                pickle.dump(sentences, f, protocol=-1)
        else:
            with open(pickled_file_path, "rb") as f:
                sentences = pickle.load(f)
        return sentences

    def _read_txt(self, file_path):
        df = pd.read_csv(file_path,
                         sep=' ',
                         skip_blank_lines=False,
                         header=None).fillna(self._unknown_word)
        # Filter out the DOCSTART lines
        df = df[~df[0].str.contains("DOCSTART")]
        return df

    def _get_sentences(self, df):
        current_rows = []
        # list of list of tuples
        sentences = []

        for i in tqdm(range(len(df))):
            row = df.values[i]
            if row[0] != self._unknown_word:
                current_rows.append(row)
            else:
                if len(current_rows) > 2:
                    _temp_df = pd.DataFrame(current_rows)
                    sentences.append(list(zip(_temp_df[self._text_col].values, _temp_df[self._ner_tag_col].values)))
                    current_rows = []
        return sentences

    def _get_words(self, sentences):
        words = set()
        for s in sentences:
            [words.add(t[0]) for t in s]
        return list(words), len(words)

    def _get_tags(self, sentences):
        tags = set()
        for s in sentences:
            [tags.add(t[1]) for t in s]
        return list(tags), len(tags)

    def _get_max_length(self, sentences):
        return max([len(s) for s in sentences])


class CoNLL2003DatasetV0(CoNLLLoader):
    NAME = "CoNLL2003DatasetV0"
    def __init__(self,
                 train_file_path,
                 val_file_path,
                 test_file_path,
                 unknown_word='unk',
                 text_col=None,
                 ner_tag_col=None,
                 cache_dir=None,
                 delete_cache=False):
        CoNLLLoader.__init__(self,
                             unknown_word=unknown_word,
                             text_col=text_col,
                             ner_tag_col=ner_tag_col)
        self._text_col = text_col
        self._ner_tag_col = ner_tag_col
        self._unknown_word = unknown_word

        if cache_dir is None:
            self.cache_dir = os.path.join(str(Path.home()), '.mozhi', "data", "cache", "ner", "conll", "2003")
        else:
            self.cache_dir = cache_dir

        if delete_cache:
            shutil.rmtree(self.cache_dir)

        train_pickle_file = self.cache_dir + "/" + "train_data.pickle"
        self.train_tuple_pairs = self.load(in_file_path=train_file_path,
                                           pickled_file_path=train_pickle_file)
        test_pickle_file = self.cache_dir + "/" + "test_data.pickle"
        self.test_tuple_pairs = self.load(in_file_path=test_file_path,
                                          pickled_file_path=test_pickle_file)
        val_pickle_file = self.cache_dir + "/" + "val_data.pickle"
        self.val_tuple_pairs = self.load(in_file_path=val_file_path,
                                         pickled_file_path=val_pickle_file)

        # Collect word and tag bags based on train data
        self.words = self._get_words(self.train_tuple_pairs)
        self.ner_tags = self._get_tags(self.train_tuple_pairs)
        self.max_length = self._get_max_length(self.train_tuple_pairs)

    @property
    def dataset_info(self) -> NERDatasetInfo:
        words, num_words = self._get_words(self.train_tuple_pairs)
        tags, num_tags = self._get_tags(self.train_tuple_pairs)
        return NERDatasetInfo(name="conll2003",
                              words=words,
                              tags=tags,
                              tot_num_tags=num_tags,
                              tot_num_words=num_words,
                              max_sent_len=self.max_length)

