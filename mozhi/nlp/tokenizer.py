import os
import spacy
import nltk
from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer


class VFTokenizer(object):
    def __init__(self,
                 nltk_tokenizer_data="tokenizers/punkt/english.pickle",
                 spacy_model_name="en_core_web_sm"):
        """

        Args:
            nltk_tokenizer_data:
            spacy_model_name: Refer `https://spacy.io/usage/models`
        """
        try:
            self._nlp = spacy.load(spacy_model_name)
        except Exception as e:
            os.system(f'python spacy download {spacy_model_name}')
            self._nlp = spacy.load(spacy_model_name)

        try:
            self._nltk = nltk.data.load(nltk_tokenizer_data)
        except Exception as e:
            nltk.download("punkt")

    def models(self):
        return ['spacy', 'nltk']

    def _sentences_nltk(self, text: str):
        return self._nltk.tokenize(text)

    def _sentences_spacy(self, text: str):
        doc = self._nlp(text)
        return [sentence.text for sentence in doc.sents]

    def sentences(self, text: str, model: str):
        """

        Args:
            text:
            model:

        Returns:

        """
        if model == 'spacy':
            return self._sentences_spacy(text=text)
        else:
            return self._sentences_nltk(text=text)

    def _tokenize_nltk(self, text: str):
        return nltk.tokenize.word_tokenize(text)

    def _tokenize_spacy(self, text: str):
        doc = self._nlp(text)
        return [token.text for token in doc]
    
    def tokenize(self, text: str, model: str):
        """

        Args:
            text:
            model:

        Returns:

        """
        if model == 'spacy':
            return self._sentences_spacy(text=text)
        else:
            return self._sentences_nltk(text=text)

    def _word_spans_nltk(self, text):
        try:
            spans = list(TreebankWordTokenizer().span_tokenize(text))
        except LookupError:
            nltk.download("punkt")
            spans = list(TreebankWordTokenizer().span_tokenize(text))
        ret = {"tokens": [{"start": s[0], "end": s[1], "text": text[s[0]:s[1]]} for s in spans]}
        return ret

    def word_span(self, text):
        return self._word_spans_nltk(text=text)