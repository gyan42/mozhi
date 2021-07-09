import importlib
import inspect
import os
import torch
from transformers import BertTokenizer, BertConfig
from ts.torch_handler.base_handler import BaseHandler

from mozhi.utils.pretty_print import logger


class InputExample(object):
    """
    A single training/test example.
    """
    def __init__(self, guid, words=None, labels=None, sentence=None):
        """Contructs a InputExample object.
        Args:
            guid (TYPE): unique id for the example
            words (TYPE): the words of the sequence
            labels (TYPE): the labels for each work of the sentence
        """
        self.guid = guid
        self.words = words
        self.labels = labels
        self.sentence = sentence
        if self.words is None and self.sentence:
            doc_tokens = []
            char_to_word_offset = []
            prev_is_whitespace = True
            # split sentence on whitepsace so that different tokens may be attributed to their original positions
            for c in self.sentence:
                if _is_whitespace(c):
                    prev_is_whitespace = True
                else:
                    if prev_is_whitespace:
                        doc_tokens.append(c)
                    else:
                        doc_tokens[-1] += c
                    prev_is_whitespace = False
                char_to_word_offset.append(len(doc_tokens) - 1)
            self.words = doc_tokens
            if self.labels is None:
                self.labels = ["O"]*len(self.words)


class InputFeatures(object):
    """
    A sigle set of input features for an example.
    """
    def __init__(self, input_ids, input_mask, segment_ids, label_ids=None, token_to_orig_index=None, orig_to_token_index=None):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_ids = label_ids
        self.token_to_orig_index = token_to_orig_index
        self.orig_to_token_index = orig_to_token_index



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

def _is_whitespace(c):
    if c == " " or c == "\t" or c == "\r" or c == "\n" or ord(c) == 0x202F:
        return True
    return False

def get_labels(path):
    if path:
        with open(path, "r") as f:
            labels = f.read().splitlines()
        if "O" not in labels:
            labels = ["O"] + labels
        return labels
    else:
        return None

class NERTorchServeHandler(BaseHandler):
    def __init__(self):
        BaseHandler.__init__(self)
        self.model = None
        self.label2idx = None
        self.device = None
        self.initialized = False
        self.manifest = None

    def initialize(self, ctx):
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_availabel() else "cpu")
        # model serialized file (model weights file)
        serialized_file = self.manifest['model']['serializedFile']
        # model def file and other model related files
        model_file = self.manifest['model']['modelFile']
        model_def_path = os.path.join(model_dir, model_file)
        model_vocab_path = os.path.join(model_dir, 'vocab.txt')
        model_bert_config_path = os.path.join(model_dir, "bert_config.json")
        model_config_path = os.path.join(model_dir, "bert_for_token_classification_config.json")
        labels_file_path = os.path.join(model_dir, "labels_file.txt")

        # loading model config file
        if os.path.isfile(model_config_path):
            with open(model_config_path, "r") as reader:
                text = reader.read()
            self.model_config_dict = json.loads(text)
            self.max_seq_length = self.model_config_dict['max_seq_length']
            self.num_special_tokens = self.model_config_dict['num_special_tokens']
        else:
            print("model_config_path doesnt exists.")
            logger.debug("model_config_path doesnt exists.")

        # loading labels
        if os.path.isfile(labels_file_path):
            self.labels = get_labels(labels_file_path) + ["<PAD>"]
            self.label2idx = {l: i for i, l in enumerate(self.labels)}
            self.idx2label = {i: l for i, l in enumerate(self.labels)}
        else:
            print("labels_file_path doesnt exists.")
            logger.debug("labels_file_path doesnt exists.")

        # loading bert config file
        if os.path.isfile(model_bert_config_path):
            self.bert_config = BertConfig.from_json_file(model_bert_config_path)
        else:
            print("bert config path doesnt exists.")
            logger.debug("bert config path doesnt exists.")

        # loading bert tokenizer
        if os.path.isfile(model_vocab_path):
            self.bert_tokenizer = BertTokenizer.from_pretrained(
                model_vocab_path, config=self.bert_config,
                do_lower_case=True # I used do_lower_case=True during training so here also True
            )
        else:
            print("vocab path doesnt exists.")
            logger.debug("vocab path doesnt exists.")

        # loading model weigths into definitions
        if os.path.isfile(model_def_path):
            module = importlib.import_module(model_file.split(".")[0])
            model_class_definitions = list_classes_from_module(module)
            if len(model_class_definitions) != 1:
                raise ValueError("Expected only one class as model definition. {}".format(model_class_definitions))

            model_class = model_class_definitions[0]
            self.model = model_class.from_pretrained(
                serialized_file,
                config=self.bert_config,
                num_labels=len(self.labels),
                classification_layer_sizes=self.model_config_dict["classification_layer_sizes"]
            )
        else:
            print("No model class found")
            logger.debug("No model class found")

        self.model.to(self.device)
        self.model.eval()
        logger.debug("Model successfully loaded.")
        self.initialized = True

    def convert_sentence_to_example(self, sentence):
        example = InputExample(guid=0, words=None, labels=None, sentence=sentence)
        return example

    def convert_example_to_feature(self, example):
        tokens = []
        token_to_orig_index = []
        orig_to_token_index = []
        for word_idx, word in enumerate(example.words):
            orig_to_token_index.append(len(tokens))
            word_tokens = self.bert_tokenizer.tokenize(word)
            if len(word_tokens) > 0:
                tokens.extend(word_tokens)
            for tok in word_tokens:
                token_to_orig_index.append(word_idx)

        if len(tokens) > self.max_seq_length - self.num_special_tokens:
            tokens = tokens[:(self.max_seq_length - self.num_special_tokens)]

        tokens += [self.bert_tokenizer.sep_token]
        segment_ids = [0]*len(tokens)
        tokens = [self.bert_tokenizer.cls_token] + tokens
        segment_ids = [0] + segment_ids
        input_ids = self.bert_tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1]*len(input_ids)
        # Zero pad up to the sequence length
        padding_length = self.max_seq_length - len(input_ids)
        input_ids += [self.bert_tokenizer.pad_token_id] * padding_length
        input_mask += [0] * padding_length
        segment_ids += [0] * padding_length
        assert len(input_ids) == self.max_seq_length
        assert len(input_mask) == self.max_seq_length
        assert len(segment_ids) == self.max_seq_length
        feature = InputFeatures(
            input_ids=input_ids,
            input_mask=input_mask,
            segment_ids=segment_ids,
            label_ids=None,
            token_to_orig_index=token_to_orig_index,
            orig_to_token_index=orig_to_token_index
        )
        return feature

    def align_out_label_with_original_sentence_tokens(self, ner_labels, example, feature):
        aligned_ner_labels = []
        for i in range(len(feature.orig_to_token_index)):
            token_idx = feature.orig_to_token_index[i]
            if token_idx < (self.max_seq_length - self.num_special_tokens):
                aligned_ner_labels.append(ner_labels[token_idx])
            else:
                aligned_ner_labels.append("O")
        return aligned_ner_labels

    def preprocess(self, data):
        text = data[0].get("data")
        if text is None:
            text = data[0].get("body")
        text = text.decode('utf-8').strip()
        logger.info("Received text: '%s'", text)
        example = self.convert_sentence_to_example(text)
        feature = self.convert_example_to_feature(example)
        model_inputs = {
            "input_ids": torch.tensor([feature.input_ids], dtype=torch.long).to(self.device),
            "attention_mask": torch.tensor([feature.input_mask], dtype=torch.long).to(self.device),
            "token_type_ids": torch.tensor([feature.segment_ids], dtype=torch.long).to(self.device),
            "labels": None
        }
        return [model_inputs, example, feature]

    def inference(self, inputs):
        model_inputs, example, feature = inputs
        logits, _, _ = self.model(**model_inputs)
        return [logits, example, feature]

    def postprocess(self, outputs):
        out_label_ids, example, feature = outputs
        prediction_label_ids = out_label_ids.detach().cpu().numpy().tolist()[0]
        sentence_input_ids = feature.input_ids[1:]
        sentence_ner_labels  = []
        for i, (ner_label_id, token_id) in enumerate(zip(prediction_label_ids, sentence_input_ids)):
            if token_id == self.bert_tokenizer.sep_token_id:
                break
            sentence_ner_labels.append(self.idx2label[ner_label_id])
        # aligning the labels with the real sentence tokens
        aligned_ner_labels = self.align_out_label_with_original_sentence_tokens(
            sentence_ner_labels, example, feature
        )
        text, entities = self.convert_to_ents_dict(example.words, aligned_ner_labels)
        return [[text, entities]]

    def convert_to_ents_dict(self, tokens, tags):
        start_offset = None
        end_offset = None
        ent_type = None
        text = " ".join(tokens)
        entities = []
        start_char_offset = 0
        for offset, (token, tag) in enumerate(zip(tokens, tags)):
            token_tag = tag
            if token_tag == "O":
                if ent_type is not None and start_offset is not None:
                    end_offset = offset - 1
                    entity = {
                        "type": ent_type,
                        "entity": " ".join(tokens[start_offset: end_offset + 1]),
                        "start_offset": start_char_offset,
                        "end_offset": start_char_offset + len(" ".join(tokens[start_offset: end_offset + 1]))
                    }
                    entities.append(entity)
                    start_char_offset += len(" ".join(tokens[start_offset: end_offset + 2])) + 1
                    start_offset = None
                    end_offset = None
                    ent_type = None
                else:
                    start_char_offset += len(tokens) + 1
            elif ent_type is None:
                ent_type = token_tag[2:]
                start_offset = offset
            elif ent_type != token_tag[2:]:
                end_offset = offset - 1
                entity = {
                    "type": ent_type,
                    "entity": " ".join(tokens[start_offset: end_offset + 1]),
                    "start_offset": start_char_offset,
                    "end_offset": start_char_offset + len(" ".join(tokens[start_offset: end_offset + 1]))
                }
                entities.append(entity)
                # start of a new entity
                ent_type = token_tag[2:]
                start_offset = offset
                end_offset = None

        # catches an entity that foes up untill the last token
        if ent_type and start_offset is not None and end_offset is not None:
            entity = {
                "type": ent_type,
                "entity": " ".join(tokens[start_offset:]),
                "start_offset": start_char_offset,
                "end_offset": start_char_offset + len(" ".join(tokens[start_offset:]))
            }
            entities.append(entity)
        return [text, entities]

_service = NERTorchServeHandler()

def handle(data, context):
    if not _service.initialized:
        _service.initialize(context)
    if data is None:
        return None
    data = _service.preprocess(data)
    data = _service.inference(data)
    data = _service.postprocess(data)
    return data