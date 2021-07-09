import torch
import torch.nn as nn
import torchmetrics
from torch.autograd import Variable
import numpy as np
from torch.nn import init
import pytorch_lightning as pl
from torchcrf import CRF
# from mozhi.model.pytorch.torch_crf import CRF
from mozhi.protocol.dataprotocol import NERPreprocessorInfo, dataclass_to_dict
from mozhi.utils.pretty_print import print_error, print_info


"""
http://www.cse.chalmers.se/~richajo/nlp2019/l6/Sequence%20tagging%20example.html

"""
class BiLSTMCRFTorch(pl.LightningModule):
    NAME = 'BiLSTMCRFTorch'
    def __init__(
            self,
            vocab_size,
            t2i,
            tot_num_tags,
            embedding_dim=64,
            hidden_dim=64,
            char_lstm_dim=25,
            char_to_ix=None,
            pre_word_embeddings=None,
            char_embedding_dim=25,
            use_crf=False,
            use_gpu=True,
            n_cap=None,
            cap_embedding_dim=None,
            char_mode="LSTM",
            *args,
            **kwargs):
        super(BiLSTMCRFTorch, self).__init__()
        self.save_hyperparameters()

        self.use_gpu = use_gpu
        # self.device = torch.device("cuda" if self.use_gpu else "cpu")
        self.word_embeddings_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size
        self.tag_to_ix = t2i
        self.n_cap = n_cap  # Capitalization feature num
        self.cap_embedding_dim = cap_embedding_dim  # Capitalization feature dim
        self.use_crf = use_crf
        self.tagset_size = len(self.tag_to_ix)
        self.out_channels = char_lstm_dim
        self.char_mode = char_mode
        self._use_crf = use_crf
        print("char_mode: %s, out_channels: %d, hidden_dim: %d, " % (char_mode, char_lstm_dim, hidden_dim))

        self.word_embeddings = nn.Embedding(num_embeddings=self.vocab_size,
                                            embedding_dim=embedding_dim)

        self.emb_dropout = nn.Dropout(0.5)

        self.lstm = nn.LSTM(input_size=embedding_dim,
                            hidden_size=hidden_dim,
                            num_layers=1,
                            bidirectional=True)

        self.hidden2tag_dropout = nn.Dropout(0.5)
        self.hidden2tag = nn.Linear(hidden_dim * 2, self.tagset_size)

        self.init_weights()
        self.init_embeddings(word_pad_idx=1)

        self.loss_fn = nn.CrossEntropyLoss(ignore_index=1)

        # self.crf = CRF(nb_labels=tot_num_tags,
        #                bos_tag_id=2,
        #                eos_tag_id=3,
        #                pad_tag_id=1,
        #                batch_first=True)

        self.crf = CRF(num_tags=tot_num_tags,
                       batch_first=True)

    @staticmethod
    def init_vf(preprocessor_data_info: NERPreprocessorInfo,
                embedding_dim=64,
                hidden_dim=64,
                char_lstm_dim=25,
                char_to_ix=None,
                pre_word_embeddings=None,
                char_embedding_dim=25,
                use_crf=False,
                use_gpu=True,
                n_cap=None,
                cap_embedding_dim=None,
                char_mode="LSTM"):
        kwargs = dataclass_to_dict(preprocessor_data_info)
        kwargs.update({"embedding_dim": embedding_dim,
                       "hidden_dim": hidden_dim,
                       "char_lstm_dim": char_lstm_dim,
                       "char_to_ix": char_to_ix,
                       "pre_word_embeddings": pre_word_embeddings,
                       "char_embedding_dim": char_embedding_dim,
                       "use_crf": use_crf,
                       "use_gpu": use_gpu,
                       "n_cap": n_cap,
                       "cap_embedding_dim": cap_embedding_dim,
                       "char_mode": char_mode})
        return BiLSTMCRFTorch(**kwargs)

    def init_weights(self):
        # to initialize all parameters from normal distribution
        # helps with converging during training
        for name, param in self.named_parameters():
            nn.init.normal_(param.data, mean=0, std=0.1)

    def init_embeddings(self, word_pad_idx):
        # initialize embedding for padding as zero
        self.word_embeddings.weight.data[word_pad_idx] = torch.zeros(self.word_embeddings_dim)

    def forward(self, sentences):
        # sentences = [batch size, sentences length]
        # embedding_out = [batch size, sentences length, embedding dim]
        embedding_out = self.emb_dropout(self.word_embeddings(sentences))
        # lstm_out = [sentence length, batch size, hidden dim * 2]
        lstm_out, _ = self.lstm(embedding_out)
        # ner_out = [sentence length, batch size, output dim]
        ner_out = self.hidden2tag(self.hidden2tag_dropout(lstm_out))
        # self.log('ner_out', ner_out.shape, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return ner_out

    def _loss(self, y, y_hat):
        if self._use_crf: #CRF
            # We return the loss value. The CRF returns the log likelihood, but we return
            # the *negative* log likelihood as the loss value.
            # PyTorch's optimizers *minimize* the loss, while we want to *maximize* the
            # log likelihood.
            loss = self.crf(y_hat, y)
            loss = -loss
        else:
            # to calculate the loss and accuracy, we flatten both prediction and true tags
            # flatten pred_tags to [batch size, sent len, output dim]
            y_hat = y_hat.view(-1, y_hat.shape[-1])
            # print_info(f"ner_logits: {y_hat.shape}")
            # flatten true_tags to [batch size * sent len]
            y = y.view(-1)
            loss = self.loss_fn(y_hat, y)
        return loss

    def training_step(self, batch, batch_idx):
        x, y = batch  # x: [BS, MAX_LEN] , y : [BS, MAX_LEN]
        ner_logits = self(x)  # BS x MAX_LEN
        if self.use_crf:
            preds = self.crf.decode(ner_logits)
        else:
            preds = ner_logits
        # preds = torch.tensor(preds)
        return self._loss(y=y, y_hat=preds)

    def validation_step(self, batch, batch_idx):
        x, y = batch
        ner_logits = self(x)
        if self.use_crf:
            preds = self.crf.decode(ner_logits)
            preds = torch.tensor(preds, device=self.device)
        else:
            preds = torch.argmax(ner_logits, dim=-1)

        val_loss = self._loss(y=y, y_hat=ner_logits)
        return {'loss': val_loss, "preds": preds, "labels": y}

    def validation_epoch_end(self, outputs):
        preds = torch.cat([x['preds'] for x in outputs])#.detach().cpu().numpy()
        labels = torch.cat([x['labels'] for x in outputs])#.detach().cpu().numpy()
        loss = torch.stack([x['loss'] for x in outputs]).mean()
        self.log('val_loss', loss, prog_bar=True)

        # print_error(preds.shape)
        # print_info(labels.shape)
        # https://torchmetrics.readthedocs.io/en/latest/references/functional.html?highlight=f1
        f1 = torchmetrics.functional.f1(preds, labels, mdmc_average='samplewise')

        # f1 = torchmetrics.functional.f1(torch.argmax(preds, dim=1), labels)
        self.log("f1", f1, prog_bar=True)
        # self.log_dict(self.metric.compute(predictions=preds, references=labels), prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        ner_logits = self(x)
        if self.use_crf:
            preds = self.crf.decode(ner_logits)
        else:
            preds = torch.argmax(ner_logits, dim=-1)
            preds = torch.tensor(preds, device=self.device)

        loss = self._loss(y=y, y_hat=ner_logits)
        return {'loss': loss, "preds": preds, "labels": y}

    def test_epoch_end(self, outputs):
        preds = torch.cat([x['preds'] for x in outputs])#.detach().cpu().numpy()
        labels = torch.cat([x['labels'] for x in outputs])#.detach().cpu().numpy()
        loss = torch.stack([x['loss'] for x in outputs]).mean()
        self.log('val_loss', loss, prog_bar=True)

        # print_error(preds.shape)
        # print_info(labels.shape)
        f1 = torchmetrics.functional.f1(preds, labels, mdmc_average='samplewise')

        # f1 = torchmetrics.functional.f1(torch.argmax(preds, dim=1), labels)
        self.log("f1", f1, prog_bar=True)
        # self.log_dict(self.metric.compute(predictions=preds, references=labels), prog_bar=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=5e-4)

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def predict(self, sentences):
        # Compute the emission scores, as above.
        ner_logits = self(sentences)

        # Apply the Viterbi algorithm to get the predictions. This implementation returns
        # the result as a list of lists (not a tensor), corresponding to a matrix
        # of shape (n_sentences, max_len).
        if self.use_crf:
            return torch.tensor(self.crf.decode(ner_logits))
        else:
            return torch.argmax(ner_logits, dim=-1)