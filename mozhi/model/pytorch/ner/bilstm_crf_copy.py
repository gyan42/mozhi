import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
from torch.nn import init
import pytorch_lightning as pl

from mozhi.protocol.dataprotocol import NERPreprocessorInfo
from mozhi.utils.pretty_print import print_error, print_info

START_TAG = "<start>"
STOP_TAG = "<stop>"


# Compute log sum exp in a numerically stable way for the forward algorithm
def log_sum_exp(smat):
    # status matrix (smat): (tagset_size, tagset_size)
    # @return (1, tagset_size)
    max_score = smat.max(dim=0, keepdim=True).values
    return (smat - max_score).exp().sum(axis=0, keepdim=True).log() + max_score

def init_embedding(input_embedding):
    """
    Initialize embedding
    """
    bias = np.sqrt(3.0 / input_embedding.size(1))
    init.uniform_(input_embedding, -bias, bias)


def init_linear(input_linear):
    """
    Initialize linear transformation
    """
    init.xavier_normal_(input_linear.weight.data)
    init.normal_(input_linear.bias.data)

def init_lstm(input_lstm):
    """
    Initialize lstm
    """
    for param in input_lstm.parameters():
        if len(param.shape) >= 2:
            init.orthogonal_(param.data)
        else:
            init.normal_(param.data)

# https://github.com/ZubinGou/NER-BiLSTM-CRF-PyTorch/blob/main/src/model.py
class BiLSTMCRFTorch(pl.LightningModule):
    NAME = 'BiLSTMCRFTorch'
    def __init__(
            self,
            preprocessor_data_info: NERPreprocessorInfo,
            embedding_dim=64,
            hidden_dim=64,
            char_lstm_dim=25,
            char_to_ix=None,
            pre_word_embeds=None,
            char_embedding_dim=25,
            use_gpu=True,
            n_cap=None,
            cap_embedding_dim=None,
            use_crf=False,
            char_mode="LSTM",
    ):
        super(BiLSTMCRFTorch, self).__init__()
        self.use_gpu = use_gpu
        # self.device = torch.device("cuda" if self.use_gpu else "cpu")
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.vocab_size = preprocessor_data_info.vocab_size
        self.tag_to_ix = preprocessor_data_info.t2i
        self.n_cap = n_cap  # Capitalization feature num
        self.cap_embedding_dim = cap_embedding_dim  # Capitalization feature dim
        self.use_crf = use_crf
        self.tagset_size = len(self.tag_to_ix)
        self.out_channels = char_lstm_dim
        self.char_mode = char_mode

        print("char_mode: %s, out_channels: %d, hidden_dim: %d, " % (char_mode, char_lstm_dim, hidden_dim))

        # if self.n_cap and self.cap_embedding_dim:
        #     self.cap_embeds = nn.Embedding(self.n_cap, self.cap_embedding_dim)
        #     torch.nn.init.xavier_uniform_(self.cap_embeds.weight)

        # if char_embedding_dim is not None:
        #     self.char_lstm_dim = char_lstm_dim
        #     self.char_embeds = nn.Embedding(len(char_to_ix), char_embedding_dim)
        #     torch.nn.init.xavier_uniform_(self.char_embeds.weight)
        #     if self.char_mode == "LSTM":
        #         self.char_lstm = nn.LSTM(char_embedding_dim, char_lstm_dim, num_layers=1, bidirectional=True)
        #         init_lstm(self.char_lstm)
        #     if self.char_mode == "CNN":
        #         self.char_cnn3 = nn.Conv2d(
        #             in_channels=1,
        #             out_channels=self.out_channels,
        #             kernel_size=(3, char_embedding_dim),
        #             padding=(2, 0),
        #         )

        self.word_embeds = nn.Embedding(num_embeddings=self.vocab_size,
                                        embedding_dim=embedding_dim)

        # if pre_word_embeds is not None:
        #     self.pre_word_embeds = True
        #     self.word_embeds.weight = nn.Parameter(torch.FloatTensor(pre_word_embeds))
        # else:
        #     self.pre_word_embeds = False

        self.dropout = nn.Dropout(0.5)

        # if self.n_cap and self.cap_embedding_dim:
        #     if self.char_mode == "LSTM":
        #         self.lstm = nn.LSTM(
        #             embedding_dim + char_lstm_dim * 2 + cap_embedding_dim,
        #             hidden_dim,
        #             bidirectional=True,
        #             )
        #     if self.char_mode == "CNN":
        #         self.lstm = nn.LSTM(
        #             embedding_dim + self.out_channels + cap_embedding_dim,
        #             hidden_dim,
        #             bidirectional=True,
        #             )
        # else:
        #     if self.char_mode == "LSTM":
        #         self.lstm = nn.LSTM(embedding_dim + char_lstm_dim * 2, hidden_dim, bidirectional=True)
        #     if self.char_mode == "CNN":
        #         self.lstm = nn.LSTM(embedding_dim + self.out_channels, hidden_dim, bidirectional=True)

        # self.lstm = nn.LSTM(embedding_dim + char_lstm_dim * 2, hidden_dim, bidirectional=True)
        self.lstm = nn.LSTM(input_size=embedding_dim,
                            hidden_size=hidden_dim,
                            num_layers=1,
                            bidirectional=True)
        init_lstm(self.lstm)

        # # high way
        # self.hw_trans = nn.Linear(self.out_channels, self.out_channels)
        # self.hw_gate = nn.Linear(self.out_channels, self.out_channels)
        # self.h2_h1 = nn.Linear(hidden_dim * 2, hidden_dim)
        # self.tanh = nn.Tanh()
        # init_linear(self.h2_h1)
        # init_linear(self.hw_gate)
        # init_linear(self.hw_trans)
        self.hidden2tag = nn.Linear(hidden_dim * 2, self.tagset_size)
        init_linear(self.hidden2tag)

        if self.use_crf:
            self.transitions = nn.Parameter(torch.randn(self.tagset_size, self.tagset_size))
            self.transitions.data[:, self.tag_to_ix[START_TAG]] = -10000
            self.transitions.data[self.tag_to_ix[STOP_TAG], :] = -10000

    def _score_sentence(self, feats, tags):
        # Gives the score of a provided tag sequence
        # tags is ground_truth, a list of ints, length is len(sentence)
        # feats is a 2D tensor, len(sentence) * tagset_size
        r = torch.LongTensor(range(feats.size()[0])).to(self.device)
        pad_start_tags = torch.cat([torch.LongTensor([self.tag_to_ix[START_TAG]]).to(self.device), tags])
        pad_stop_tags = torch.cat([tags, torch.LongTensor([self.tag_to_ix[STOP_TAG]]).to(self.device)])

        score = torch.sum(self.transitions[pad_start_tags, pad_stop_tags]) + torch.sum(feats[r, tags])
        return score

    def _get_lstm_features(self, sentence, chars, caps, chars2_length, d):

        # if self.char_mode == "LSTM":
        #     # self.char_lstm_hidden = self.init_lstm_hidden(dim=self.char_lstm_dim, bidirection=True, batchsize=chars.size(0))
        #     chars_embeds = self.char_embeds(chars).transpose(0, 1)
        #     packed = torch.nn.utils.rnn.pack_padded_sequence(chars_embeds, chars2_length)
        #     lstm_out, _ = self.char_lstm(packed)
        #     outputs, output_lengths = torch.nn.utils.rnn.pad_packed_sequence(lstm_out)
        #     outputs = outputs.transpose(0, 1)
        #     chars_embeds_temp = Variable(torch.FloatTensor(torch.zeros(
        #         (outputs.size(0), outputs.size(2))))).to(self.device)
        #     for i, index in enumerate(output_lengths):
        #         chars_embeds_temp[i] = torch.cat((
        #             outputs[i, index - 1, :self.char_lstm_dim],
        #             outputs[i, 0, self.char_lstm_dim:],
        #         ))
        #     chars_embeds = chars_embeds_temp.clone()
        #     for i in range(chars_embeds.size(0)):
        #         chars_embeds[d[i]] = chars_embeds_temp[i]
        #
        # if self.char_mode == "CNN":
        #     chars_embeds = self.char_embeds(chars).unsqueeze(1)
        #     chars_cnn_out3 = self.char_cnn3(chars_embeds)
        #     chars_embeds = nn.functional.max_pool2d(chars_cnn_out3,
        #                                             kernel_size=(chars_cnn_out3.size(2),
        #                                                          1)).view(chars_cnn_out3.size(0), self.out_channels)

        # t = self.hw_gate(chars_embeds) # high way
        # g = nn.functional.sigmoid(t)
        # h = nn.functional.relu(self.hw_trans(chars_embeds))
        # chars_embeds = g * h + (1 - g) * chars_embeds

        embeds = self.word_embeds(sentence)  # BS X MAX_LEN x EMB
        # if self.n_cap and self.cap_embedding_dim:
        #     cap_embedding = self.cap_embeds(caps)
        #     embeds = torch.cat((embeds, chars_embeds, cap_embedding), 1)
        # else:
        #     embeds = torch.cat((embeds, chars_embeds), 1)

        # embeds = embeds.unsqueeze(1)
        embeds = self.dropout(embeds)
        # print_error(embeds.shape)
        lstm_out, _ = self.lstm(embeds)  # BS X MAX_LEN x EMB * 2
        # print_error(lstm_out.shape)
        # lstm_out = lstm_out.view(len(sentence), self.hidden_dim * 2)
        lstm_out = self.dropout(lstm_out)  # BS X MAX_LEN x EMB * 2
        # print_error(lstm_out.shape)
        lstm_feats = self.hidden2tag(lstm_out)  # BS X MAX_LEN x NUM_TAGS
        print_error(lstm_feats.shape)
        return lstm_feats

    def _forward_alg(self, feats):
        # calculate in log domain
        # feats is len(sentence) * tagset_size
        alpha = torch.full((1, self.tagset_size), -10000.0, device=self.device)
        alpha[0][self.tag_to_ix[START_TAG]] = 0.0
        for feat in feats:
            print_error(self.transitions.shape)
            print_info(feat.shape)
            alpha = log_sum_exp(alpha.T + feat.unsqueeze(0) + self.transitions)
        return log_sum_exp(alpha.T + 0 + self.transitions[:, [self.tag_to_ix[STOP_TAG]]]).flatten()[0]

    def viterbi_decode(self, feats):
        backtrace = []
        alpha = torch.full((1, self.tagset_size), -10000.0, device=self.device)
        alpha[0][self.tag_to_ix[START_TAG]] = 0
        for feat in feats:
            smat = (alpha.T + feat.unsqueeze(0) + self.transitions)  # (tagset_size, tagset_size)
            backtrace.append(smat.argmax(0))  # column_max
            alpha = log_sum_exp(smat)
        # backtrack
        smat = alpha.T + 0 + self.transitions[:, [self.tag_to_ix[STOP_TAG]]]
        best_tag_id = smat.flatten().argmax().item()
        best_path = [best_tag_id]
        for bptrs_t in reversed(backtrace[1:]):  # ignore START_TAG
            best_tag_id = bptrs_t[best_tag_id].item()
            best_path.append(best_tag_id)
        return log_sum_exp(smat).item(), best_path[::-1]  # item() return list?

    def neg_log_likelihood(self, sentence, tags, chars=None,
                           caps=None, chars2_length=None, d=None):
        # sentence, tags is a list of ints
        # features is a 2D tensor, len(sentence) * self.tagset_size
        feats = self._get_lstm_features(sentence, chars, caps, chars2_length, d)

        if self.use_crf:
            forward_score = self._forward_alg(feats)
            gold_score = self._score_sentence(feats, tags)
            return forward_score - gold_score
        else:
            tags = Variable(tags)
            scores = nn.functional.cross_entropy(feats, tags)
            return scores

    def forward(self, sentence, chars=None, caps=None, chars2_length=None, d=None):
        feats = self._get_lstm_features(sentence, chars, caps, chars2_length, d)
        # viterbi to get tag_seq
        if self.use_crf:
            score, tag_seq = self.viterbi_decode(feats)
        else:
            score, tag_seq = torch.max(feats, 1)
            tag_seq = tag_seq.cpu().tolist()

        return score, tag_seq

    def training_step(self, batch, batch_idx):
        x, y = batch  # x: [BS x MAX_LEN] , y : [BS x MAX_LEN x NUM_TAGS]
        loss = self.neg_log_likelihood(x, y)  # BS x MAX_LEN x NUM_TAGS
        return loss

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