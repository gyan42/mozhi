from mozhi.preprocessor.conll_sentence import SentencePreprocessor


# Add new datasets to the list here
from mozhi.preprocessor.hf_tokenizer import HFTokenizer

preprocessor = [SentencePreprocessor, HFTokenizer]

PREPROCESSOR_OBJ_MAP = {d.NAME: d for d in preprocessor}