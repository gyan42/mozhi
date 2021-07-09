import torch
import torchmetrics
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

import pytorch_lightning as pl
# from pytorch_lightning.metrics.functional import accuracy, f1_score
from keras.preprocessing.sequence import pad_sequences
from mozhi.protocol.dataprotocol import NERPreprocessorInfo
from mozhi.utils.pretty_print import print_error, print_info


class LSTMTagger(pl.LightningModule):
    NAME = "LSTMTagger"
    def __init__(self,
                 preprocessor_data_info: NERPreprocessorInfo = None,
                 embedding_dim=32,
                 hidden_dim=64):
        super(LSTMTagger, self).__init__()

        vocab_size = preprocessor_data_info.vocab_size
        num_tags = preprocessor_data_info.tot_num_tags
        sentence_max_length = preprocessor_data_info.max_sent_len

        self.hidden_dim = hidden_dim
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)
        # The linear layer that maps from hidden state space to tag space
        self.hidden2tag = nn.Linear(hidden_dim, num_tags)

    def forward(self, sentences):
        embeds = self.word_embeddings(sentences)
        lstm_out, _ = self.lstm(embeds)
        logits = self.hidden2tag(lstm_out)
        return logits

    def training_step(self, batch, batch_idx):
        x, y = batch  # x: [BS x MAX_LEN] , y : [BS x MAX_LEN x NUM_TAGS]
        y_hat = self(x)  # BS x MAX_LEN x NUM_TAGS
        y_hat = y_hat.permute(0, 2, 1)  # BS x NUM_TAGS x MAX_LEN
        loss = F.log_softmax(y_hat, dim=1)
        # loss = nn.functional.cross_entropy(y_hat, y)
        # y = y.permute(0, 2, 1)  # BS x NUM_TAGS x MAX_LEN
        # loss = nn.CrossEntropyLoss()(y_hat, y)
        # loss = nn.NLLLoss()(y_hat, y)
        loss = torch.mean(loss)
        return {'loss': loss}

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        y_hat = y_hat.permute(0, 2, 1)
        loss = nn.CrossEntropyLoss()(y_hat, y)
        result = pl.EvalResult()
        result.log('val_f1', torchmetrics.functional.f1_score(torch.argmax(y_hat, dim=1), y), prog_bar=True)
        return result

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        y_hat = y_hat.permute(0, 2, 1)
        loss = nn.CrossEntropyLoss()(y_hat, y)
        return {'test_f1': torchmetrics.functional.f1_score(torch.argmax(y_hat, dim=1), y)}

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=5e-4)
