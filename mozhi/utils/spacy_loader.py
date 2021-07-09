import spacy
import os

nlp = None


def get_spacy_nlp_instance(model="en_core_web_sm", reinitiaze: bool=False):
    global nlp
    try:
        if nlp is None or reinitiaze:
            nlp = spacy.load(model)
    except Exception as e:
        os.system(f'python -m spacy download {model}')
        nlp = spacy.load(model)
    return nlp