import os
import time
import fire

from mozhi.bin.estimators.vf_ner import VFNER
from mozhi.utils.pretty_print import print_info


def main(experiment_name: str,
         preprocessor_name: str,
         model_name: str,
         sentence: str,
         model_chk_pth: str,
         preprocessor_dir: str):
    """

    Args:
        experiment_name:
        preprocessor_name: Preprocessor Name
        model_name: Model Name
        sentence: Sentence to Predict
        model_chk_pth: Model checkpoint path

    Returns:

    """
    start = time.time()
    tagger = VFNER(experiment_name=experiment_name,
                   preprocessor_name=preprocessor_name,
                   model_name=model_name,
                   preprocessor_dir=os.path.expanduser(preprocessor_dir),
                   model_chk_pth=os.path.expanduser(model_chk_pth),
                   is_tf_model=False)
    print(tagger.inference(sentence=sentence))
    print_info(f"Time taken to infer {time.time() - start} seconds or {(time.time() - start)/60} mins")


if __name__ == "__main__":
    fire.Fire((main))