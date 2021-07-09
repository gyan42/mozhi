# https://github.com/plasticityai/magnitude
from pymagnitude import *
from pathlib import Path

mag_vec_file_handler = None


def get_mag_word_vec(word, file_path: Path=Path("~/.mozhi/data/wordvec/")):
    global mag_vec_file_handler
    if mag_vec_file_handler is None:
        mag_vec_file_handler = Magnitude(MagnitudeUtils.download_model('word2vec/heavy/GoogleNews-vectors-negative300'),
                                         download_dir=file_path)
    else:
        if word in mag_vec_file_handler:
            return mag_vec_file_handler.query(word)
        else:
            return None
