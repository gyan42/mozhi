import logging
import os
import fire
import torch
import ts
from ts.torch_handler.base_handler import BaseHandler
from transformers import AutoModelForTokenClassification
from transformers import AutoTokenizer

logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class HFNERHandler(BaseHandler):
    """
    A custom model handler implementation.
    """

    def __init__(self):
        self._context = None
        self.initialized = False
        self.explain = False
        self.input_text = None
        self.tokenizer = None


    def initialize(self, context): # : ts.context.Context
        """
        Initialize model. This will be called during model loading time
        :param context: Initial context contains model server system properties.
        :return:
        """

        if type(context) is dict:
            properties = context["system_properties"]
        else:
            properties = context.system_properties

        model_dir = properties.get("model_dir")
        logger.debug(f"Loading model from {model_dir}")
        self.model = AutoModelForTokenClassification.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)

        self.initialized = True

    def preprocess(self, sequence_text):
        """
        Transform raw input into model input data.
        :param batch: list of raw requests, should match batch size
        :return: list of preprocessed model input data
        """
        preprocessed_data = self.tokenizer.encode(sequence_text, return_tensors="pt")
        print("Preprocessed data: \n" + str(preprocessed_data))

        return preprocessed_data


    def inference(self, model_input):
        """
        Internal inference methods
        :param model_input: transformed model input data
        :return: list of inference output in NDArray
        """
        # Do some inference call to engine here and return output
        model_input = torch.tensor(model_input)
        outputs = self.model(model_input).logits
        predictions = torch.argmax(outputs, dim=2)
        return predictions

    def postprocess(self, predictions, tokens):
        """
        Return inference result.
        :param inference_output: list of inference output
        :return: list of predict results
        """
        res = []
        for token, prediction in zip(tokens, predictions[0].numpy()):
            res.append((token, self.model.config.id2label[prediction]))

        logger.error(res)
        return res

    def handle(self, data, context):
        """
        Invoke by TorchServe for prediction request.
        Do pre-processing of data, prediction using model and postprocessing of prediciton output
        :param data: [{body: bytearray()}]Input data for prediction
        :param context: Initial context contains model server system properties.
        :return: prediction output
        """
        logger.error(data)

        res = []
        for d in data:  # TODO how to batch it?
            logger.error(d)
            sequence_text = d.get("data")
            if sequence_text is None:
                sequence_text = d.get("body")

            # To handle Vue Axios Post method
            if type(sequence_text) == dict:
                sequence_text = sequence_text["text"]

            if type(sequence_text) != str:
                sequence_text = sequence_text.decode('UTF-8')
            tokens = self.tokenizer.tokenize(self.tokenizer.decode(self.tokenizer.encode(sequence_text)))
            input = self.preprocess(sequence_text)
            predictions = self.inference(input)
            res.append(self.postprocess(predictions, tokens))
        return res


def main(unserialized_mar_dir, sequence):
    """

    Args:
        unserialized_mar_dir:
        sequence:

    Returns:

    """
    handler = HFNERHandler()
    handler.initialize(context={"system_properties": {"model_dir": os.path.expanduser(unserialized_mar_dir)}})
    res = handler.handle(data=[{"data": sequence}], context=None)
    print(res)


if __name__ == "__main__":
    fire.Fire(main)