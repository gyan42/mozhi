import fire
import time
from mozhi.bin.urn.datasets_urn import DATASET_OBJ_MAP
from mozhi.bin.urn.models_urn import TF_MODEL_OBJECT_MAP, PYTORCH_MODEL_OBJECT_MAP
from mozhi.bin.urn.preprocessor_urn import PREPROCESSOR_OBJ_MAP
from mozhi.preprocessor.ipreprocessor import IPreprocessor
from mozhi.protocol.dataprotocol import NERModelInfo
from mozhi.config.config import settings
from mozhi.utils.pretty_print import print_info, print_error, print_warn
import torch
# https://towardsdatascience.com/how-to-deploy-your-pytorch-models-with-torchserve-2452163871d3


class VFNER(object):
    def __init__(self,
                 experiment_name: str,
                 preprocessor_name: str,
                 model_name: str,
                 preprocessor_dir: str,
                 model_chk_pth: str,
                 is_tf_model: bool):
        self._is_tf_model = is_tf_model
        self._model_chk_pth = model_chk_pth
        self._model_name = model_name

        self._preprocessor: IPreprocessor = PREPROCESSOR_OBJ_MAP[preprocessor_name].load(file_path=preprocessor_dir + "/"  +
                                                                                             PREPROCESSOR_OBJ_MAP[preprocessor_name].NAME)
        # model = TF_MODEL_OBJECT_MAP[model_name].init_vf(preprocessor_data_info=preprocessor.get_preprocessor_info(),
        #                                                 **settings.models[model_name])
        self._model = self.load_model()

    def load_model(self):
        if self._is_tf_model:
            return self.load_tf_model()
        else:
            return self.load_pytorch_model()

    def load_tf_model(self):
        pass

    def load_pytorch_model(self):
        return PYTORCH_MODEL_OBJECT_MAP[self._model_name].load_from_checkpoint(self._model_chk_pth)

    def preprocess(self, data):
        data = self._preprocessor.tokenize(sentence=data)
        print_info("Preprocessed data: \n" + str(data))
        return data

    def inference(self, sentence):
        tokens = self.preprocess(data=sentence)
        # pred = self._model(tokens)
        # pred = torch.argmax(preds, dim=-1)[0]
        pred = self._model.predict(torch.tensor(tokens))[0]
        pred = pred[:len(sentence.split(" "))]
        print_info("Predicted results: \n" + str(pred))
        print_warn(self._preprocessor._tag2idx)
        return self._preprocessor.ids2labels(pred)

    def postprocess(self, data):
        return torch.argmax(data, dim=-1)