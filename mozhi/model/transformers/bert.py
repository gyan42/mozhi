# https://chriskhanhtran.github.io/posts/spanberta-bert-for-spanish-from-scratch/
# https://chriskhanhtran.github.io/posts/named-entity-recognition-with-transformers/

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertModel


class BertCRF(BertModel):
    """
    Simply doing token classification over bert outputs.
    """
    def __init__(self, config, num_labels, classification_layer_sizes=[]):
        super(BertCRF, self).__init__(config)
        self.num_labels = num_labels
        self.dropout_layer = nn.Dropout(config.hidden_dropout_prob)
        self.bert = BertModel(config)
        self.input_layer_sizes = [config.hidden_size] + classification_layer_sizes
        self.output_layer_size = classification_layer_sizes + [self.num_labels]
        self.classification_module = nn.ModuleList(
            nn.Linear(inp, out)
            for inp, out in zip(self.input_layer_sizes, self.output_layer_size)
        )
        self.num_linear_layer = len(classification_layer_sizes) + 1
        self.init_weights()

    def forward(
        self, input_ids, attention_mask=None, token_type_ids=None,
        position_ids=None, head_mask=None, labels=None
    ):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask
        )

        logits = outputs[0]
        for layer_idx, layer in enumerate(self.classification_module):
            if layer_idx + 1 != self.num_linear_layer:
                logits = self.dropout_layer(F.relu(layer(logits)))
            else:
                logits = layer(logits)

        # escaping cls token
        logits = logits[:, 1:, :].contiguous()
        if labels is not None:
            labels = labels[:, 1:].contiguous()
        input_ids = input_ids[:, 1:].contiguous()
        attention_mask = attention_mask[:, 1:].contiguous()

        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            # only keep active parts of the loss
            if attention_mask is not None:
                active_loss = attention_mask.view(-1) == 1
                active_logits = logits.view(-1, self.num_labels)[active_loss]
                active_labels = labels.view(-1)[active_loss]
                loss = loss_fct(active_logits, active_labels)
            else:
                loss =loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
        else:
            loss = None

        softs, out = torch.max(logits, axis=2)
        return out, labels, loss