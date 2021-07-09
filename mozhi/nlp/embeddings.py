from mozhi.utils.spacy_loader import get_spacy_nlp_instance

# https://radimrehurek.com/gensim/models/word2vec.html
from gensim.models import KeyedVectors
import gensim.downloader
import numpy as np
from tqdm import tqdm

gensim_wordvec_model = None

def _get_gensim_vec(word, model_name):
    """

    Args:
        word:
        model_name: One of the model names listed by `get_all_wordvec_models`

    Returns:

    """
    global gensim_wordvec_model
    if gensim_wordvec_model is None: # TODO what is model changes?
        gensim_wordvec_model = gensim.downloader.load(model_name)
    if word in gensim_wordvec_model:
        return gensim_wordvec_model[word]
    else:
        return None


class VFEmbeddings(object):
    @staticmethod
    def spacy(word):
        nlp = get_spacy_nlp_instance()
        return nlp.vocab[word].vector

    @staticmethod
    def list_gensim_models():
        """
        Returns:
                ['fasttext-wiki-news-subwords-300',
                 'conceptnet-numberbatch-17-06-300',
                 'word2vec-ruscorpora-300',
                 'word2vec-google-news-300',
                 'glove-wiki-gigaword-50',
                 'glove-wiki-gigaword-100',
                 'glove-wiki-gigaword-200',
                 'glove-wiki-gigaword-300',
                 'glove-twitter-25',
                 'glove-twitter-50',
                 'glove-twitter-100',
                 'glove-twitter-200',
                 '__testing_word2vec-matrix-synopsis']
        """
        return list(gensim.downloader.info()['models'].keys())

    @staticmethod
    def gensim(word, model_name):
        return _get_gensim_vec(word=word, model_name=model_name)

    @staticmethod
    # TODO: use memmap?
    def get_glove_embedding_mat(glove_path="~/.mozhi/data/wordvec/glove.6B.300d.txt"):
        print('Indexing word vectors.')

        embeddings_index = {}
        f = open(glove_path, encoding='utf-8')
        for line in tqdm(f):
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
        f.close()

        print('Found %s word vectors.' % len(embeddings_index))
        return embeddings_index