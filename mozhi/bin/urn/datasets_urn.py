from mozhi.dataset.ner.conll.hf_conll_2003 import HFConll2003Dataset
from mozhi.dataset.ner.conll.vf_conll_2003 import CoNLL2003DatasetV0


# Add new datasets to the list here
datasets = [CoNLL2003DatasetV0, HFConll2003Dataset]

# Create Dataset Name -> Dataset Object dictionary for all models
DATASET_OBJ_MAP = {d.NAME: d for d in datasets}