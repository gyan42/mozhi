# Ref: https://github.com/huggingface/datasets/blob/master/datasets/conll2003/conll2003.py
import os
from pathlib import Path

import datasets
from datasets import DownloadConfig

logger = datasets.logging.get_logger(__name__)

_CITATION = ""
_DESCRIPTION = """\

"""

_URL = "https://github.com/gyan42/model-store/raw/main/SROIE2019/"
_TRAINING_FILE = "train.txt"
_DEV_FILE = "valid.txt"
_TEST_FILE = "test.txt"


class SROIE2019Config(datasets.BuilderConfig):
    """BuilderConfig for SROIE2019"""

    def __init__(self, **kwargs):
        """BuilderConfig for SROIE2019.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SROIE2019Config, self).__init__(**kwargs)


class SROIE2019(datasets.GeneratorBasedBuilder):
    """SROIE2019 dataset."""

    BUILDER_CONFIGS = [
        SROIE2019Config(name="SROIE2019", version=datasets.Version("1.0.0"), description="SROIE2019 dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "company", "date", "address", "total", "O"
                            ]
                        )
                    )
                }
            ),
            supervised_keys=None,
            homepage="",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                if line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    # SROIE2019 tokens are space separated
                    splits = line.split(" ")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }


if __name__ == '__main__':
    config = DownloadConfig(cache_dir=os.path.join(str(Path.home()), '.mozhi'))
    dataset = SROIE2019().download_and_prepare(download_config=config)