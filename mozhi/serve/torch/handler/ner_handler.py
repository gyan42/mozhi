import importlib
import inspect
import os
import logging
import torch
import pickle
from abc import ABC

import ts
from ts.torch_handler.base_handler import BaseHandler
from ts.torch_handler.text_handler import TextHandler

from mozhi.preprocessor.ipreprocessor import IPreprocessor
from mozhi.bin.urn.models_urn import TF_MODEL_OBJECT_MAP, PYTORCH_MODEL_OBJECT_MAP
from mozhi.bin.urn.preprocessor_urn import PREPROCESSOR_OBJ_MAP

logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


def load(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def list_classes_from_module(module, parent_class=None):
    """
    Parse user defined module to get all model service classes in it.

    :param module:
    :param parent_class:
    :return: List of model service class definitions
    """

    # Parsing the module to get all defined classes
    classes = [cls[1] for cls in inspect.getmembers(module, lambda member: inspect.isclass(member) and
                                                    member.__module__ == module.__name__)]
    # filter classes that is subclass of parent_class
    if parent_class is not None:
        return [c for c in classes if issubclass(c, parent_class)]

    return classes


class NERHandler(BaseHandler):
    """
    A custom model handler implementation.
    """

    def __init__(self):
        self._context = None
        self.initialized = False
        self.explain = False
        self.input_text = None
        self._preprocessor = None

    def _load_pickled_model(self, model_dir, model_file, model_pt_path):
        """
        Loads the pickle file from the given model path.

        Args:
            model_dir (str): Points to the location of the model artefacts.
            model_file (.py): the file which contains the model class.
            model_pt_path (str): points to the location of the model pickle file.

        Raises:
            RuntimeError: It raises this error when the model.py file is missing.
            ValueError: Raises value error when there is more than one class in the label,
                        since the mapping supports only one label per class.

        Returns:
            serialized model file: Returns the pickled pytorch model file
        """
        model_def_path = os.path.join(model_dir, model_file)
        logger.error("===============model_def_path " + model_def_path)

        if not os.path.isfile(model_def_path):
            raise RuntimeError("Missing the model.py file")

        logger.error("===============model_class_definitions" + importlib.import_module(model_file.split(".")[0]))
        module = importlib.import_module(model_file.split(".")[0])
        model_class_definitions = list_classes_from_module(module)
        logger.error("===============model_class_definitions" + model_class_definitions)

        if len(model_class_definitions) != 1:
            raise ValueError(
                "Expected only one class as model definition. {}".format(
                    model_class_definitions
                )
            )

        model_class = model_class_definitions[0]
        logger.error("===============model_class" + model_class)
        model = model_class()
        if model_pt_path:
            state_dict = torch.load(model_pt_path, map_location=self.device)
            model.load_state_dict(state_dict)
        return model

    def _load_torchscript_model(self, model_pt_path):
        """Loads the PyTorch model and returns the NN model object.

        Args:
            model_pt_path (str): denotes the path of the model file.

        Returns:
            (NN Model Object) : Loads the model object.
        """
        logger.error("self.device===============>" + str(self.device))

        # model = torch.jit.load(model_pt_path, map_location=self.device)
        model = torch.jit.load(model_pt_path)
        logger.error("_load_torchscript_model===============>" + model_pt_path)

        return model

    def initialize(self, context: ts.context.Context):
        """
        Initialize model. This will be called during model loading time
        :param context: Initial context contains model server system properties.
        :return:
        """

        logger.error("===================>context" + str(context))
        properties = context.system_properties
        logger.error("===================>properties" + str(properties))
        model_dir = properties.get("model_dir")

        logger.info("*" * 100)

        self._preprocessor = load(os.path.join(model_dir, "NaiveSentencePreprocessor"))

        logger.info("=" * 100)
        logger.error(self._preprocessor.id2label(3))
        logger.info("*" * 100)
        logger.error(model_dir)


        self.map_location = "cuda" if torch.cuda.is_available() and properties.get("gpu_id") is not None else "cpu"
        self.device = torch.device(
            self.map_location + ":" + str(properties.get("gpu_id"))
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else self.map_location
        )
        self.manifest = context.manifest

        logger.error("===================>context.manifest" + str(context.manifest))

        """
        .pt
        {'createdOn': '11/06/2021 21:27:42', 'runtime': 'python', 'model': {'modelName': 'bilstmcrf', 
        'serializedFile': 'bilstmcrftorch.pt', 'handler': 'ner_handler.py', 'modelFile': 'bilstm_crf_torch.py', 
        'modelVersion': '1.0'}, 'archiverVersion': '0.4.0'}
        """



        model_pt_path = None
        if "serializedFile" in self.manifest["model"]:
            serialized_file = self.manifest["model"]["serializedFile"]
            model_pt_path = os.path.join(model_dir, serialized_file)

        logger.error("model_pt_path===============>" + model_pt_path)
        # model def file
        model_file = self.manifest["model"].get("modelFile", "")
        logger.error("model_file===============>" + model_pt_path)

        if model_file:
            logger.debug("Loading eager model")
            self.model = self._load_pickled_model(model_dir, model_file, model_pt_path)
            self.model.to(self.device)
        else:
            logger.debug("Loading torchscript model")
            if not os.path.isfile(model_pt_path):
                raise RuntimeError("Missing the model.pt file")

            self.model = self._load_torchscript_model(model_pt_path)

        self.model.eval()

        logger.debug('Model file %s loaded successfully', model_pt_path)

        # # Load class mapping for classifiers
        # mapping_file_path = os.path.join(model_dir, "index_to_name.json")
        # self.mapping = load_label_mapping(mapping_file_path)

        self.initialized = True
        #  load the model, refer 'custom handler class' above for details

    def preprocess(self, data):
        """
        Transform raw input into model input data.
        :param batch: list of raw requests, should match batch size
        :return: list of preprocessed model input data
        """
        # Take the input data and make it inference ready
        preprocessed_data = data[0].get("data")
        if preprocessed_data is None:
            preprocessed_data = data[0].get("body")
        logger.info("=" * 100 + "preprocessed_data " + str(preprocessed_data))

        preprocessed_data = preprocessed_data.decode('UTF-8')
        preprocessed_data = self._preprocessor.tokenize(sentence=preprocessed_data)
        print("Preprocessed data: \n" + str(preprocessed_data))

        return preprocessed_data


    def inference(self, model_input):
        """
        Internal inference methods
        :param model_input: transformed model input data
        :return: list of inference output in NDArray
        """
        # Do some inference call to engine here and return output
        logger.info("=" * 100 + "inference " + str(model_input))
        model_input = torch.tensor(model_input)
        model_output = self.model(model_input)
        logger.info("=" * 100 + "model_output " + str(model_output))
        model_output = torch.argmax(model_output, dim=-1)
        logger.info("=" * 100 + "model_output " + str(model_output[0]))
        return model_output

    def postprocess(self, inference_output):
        """
        Return inference result.
        :param inference_output: list of inference output
        :return: list of predict results
        """
        # Take output from network and post-process to desired format
        # postprocess_output = inference_output
        # return torch.argmax(inference_output, dim=-1)
        return [self._preprocessor.ids2labels(p) for p in inference_output]


    def handle(self, data, context):
        """
        Invoke by TorchServe for prediction request.
        Do pre-processing of data, prediction using model and postprocessing of prediciton output
        :param data: [{body: bytearray()}]Input data for prediction
        :param context: Initial context contains model server system properties.
        :return: prediction output
        """

        logger.info("=" * 100 + "handle " + str(data))
        model_input = self.preprocess(data)

        model_output = self.inference(model_input)
        res = self.postprocess(model_output)
        logger.info("*" * 100 + str(res))
        return res