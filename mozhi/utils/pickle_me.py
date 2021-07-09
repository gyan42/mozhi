import os
import pickle
import pathlib


class PickleMe(object):
    @staticmethod
    def dump(file_path, obj):
        parent_dir = pathlib.Path(file_path).parent
        os.makedirs(parent_dir, exist_ok=True)

        # create a pickle file
        with open(file_path, 'wb') as f:
            # pickle the dictionary and write it to file
            pickle.dump(obj, f)

    @staticmethod
    def load(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
