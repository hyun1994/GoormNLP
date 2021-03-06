import torch
import torch.nn as nn
import copy
import math
from torch.autograd import Variable
import numpy as np
import collections
import torch.nn.functional as F


def clones(module, N):
    "Produce N identical layers."

    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])


def subsequent_mask(size):
    "Mask out subsequent positions."
    attn_shape = (1, size, size)
    subsequent_mask = np.triu(np.ones(attn_shape), k=1).astype('uint8')
    return torch.from_numpy(subsequent_mask) == 0


def attention(query, key, value, mask=None, dropout=None):
    "Compute 'Scaled Dot Product Attention'"
    key_transpose = torch.transpose(key,-2,-1)
    matmul_result = torch.matmul(query, key_transpose)
    d_k = key.size()[-1]
    scores = matmul_result/math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask==0, -1e20)
    p_attn = F.softmax(scores, dim=-1)
    if dropout is not None:
        p_attn = dropout(p_attn)
    return torch.matmul(p_attn, value), p_attn

    # d_k = query.size(-1)

    # scores = torch.matmul(query, key.transpose(-2, -1)) \
    #          / math.sqrt(d_k)


    # if mask is not None:
    #     scores = scores.masked_fill(mask == 0, -1e20)
    # p_attn = F.softmax(scores, dim=-1)
    # if dropout is not None:
    #     p_attn = dropout(p_attn)
    # return torch.matmul(p_attn, value), p_attn

class EncoderLayer(nn.Module):
    "Encoder is made up of self-attn and feed forward (defined below)"

    def __init__(self, size, self_attn, feed_forward, dropout):
        super(EncoderLayer, self).__init__()
        self.self_attn = self_attn
        self.feed_forward = feed_forward
        self.sublayer = clones(SublayerConnection(size, dropout), 2)
        self.size = size

    def forward(self, x, mask):
        "Follow Figure 1 (left) for connections"

        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))
        return self.sublayer[1](x, self.feed_forward)

class Encoder(nn.Module):
    "Core encoder is a stack of N layers"
    
    def __init__(self, layer, N):
        super(Encoder, self).__init__()
        self.layers = clones(layer, N)
        self.norm = LayerNorm(layer.size)

    def forward(self, x, mask):
        "Pass the input (and mask) through each layer in turn"
        
        for layer in self.layers:
            x = layer(x, mask)
        #return x
        return self.norm(x)

class LayerNorm(nn.Module):
    "Construct a layernorm module (See citation for details)."

    def __init__(self, features, eps=1e-6):
        super(LayerNorm, self).__init__()
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        self.eps = eps

    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, unbiased=False, keepdim=True)
        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2


class SublayerConnection(nn.Module):
    """
    A residual connection followed by a layer norm.
    Note for code simplicity the norm is first as opposed to last.
    """

    def __init__(self, size, dropout):
        super(SublayerConnection, self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer):
        "Apply residual connection to any sublayer with the same size."
        #return self.norm(x + self.dropout(sublayer(x)))
        return x + self.dropout(sublayer(self.norm(x)))


class DecoderLayer(nn.Module):
    "Decoder is made of self-attn, src-attn, and feed forward (defined below)"

    def __init__(self, size, self_attn, src_attn, feed_forward, dropout):
        super(DecoderLayer, self).__init__()
        self.size = size
        self.self_attn = self_attn
        self.src_attn = src_attn
        self.feed_forward = feed_forward
        self.sublayer = clones(SublayerConnection(size, dropout), 3)

    def forward(self, x, memory, src_mask, tgt_mask):
        "Follow Figure 1 (right) for connections."
        m = memory
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, tgt_mask))
        
        src_mask = torch.unsqueeze(src_mask,1)
        # src_mask = (src_mask-1)*-1

        x = self.sublayer[1](x, lambda x: self.src_attn(x, m, m, src_mask))

        return self.sublayer[2](x, self.feed_forward)


class Decoder(nn.Module):
    "Generic N layer decoder with masking."

    def __init__(self, tgt_vocab_size, n_head, d_model, d_ff, n_layer, dropout):
        super(Decoder, self).__init__()
        c = copy.deepcopy
        attn = MultiHeadedAttention(n_head, d_model)
        ff = PositionwiseFeedForward(d_model, d_ff, dropout)

        layer = DecoderLayer(d_model, c(attn), c(attn), c(ff), dropout)
        self.layers = clones(layer, n_layer)
        self.norm = LayerNorm(layer.size)
        self.embeddings = Embeddings(d_model, tgt_vocab_size)

    def forward(self, x, memory, src_mask, tgt_mask):
        x = self.embeddings(x)

        for layer in self.layers:
            x = layer(x, memory, src_mask, tgt_mask)

        return self.norm(x)


class MultiHeadedAttention(nn.Module):
    def __init__(self, h, d_model, dropout=0.1):
        "Take in model size and number of heads."
        super(MultiHeadedAttention, self).__init__()
        assert d_model % h == 0
        # We assume d_v always equals d_k
        self.d_k = d_model // h
        self.h = h
        self.linears = clones(nn.Linear(d_model, d_model), 4)
        self.attn = None
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, query, key, value, mask=None):
        "Implements Figure 2"
        if mask is not None:
            # Same mask applied to all h heads.
            mask = mask.unsqueeze(1)
        nbatches = query.size(0)

        # 1) Do all the linear projections in batch from d_model => h x d_k
        query, key, value = \
            [l(x).view(nbatches, -1, self.h, self.d_k).transpose(1, 2)
             for l, x in zip(self.linears, (query, key, value))]

        # 2) Apply attention on all the projected vectors in batch.
        x, self.attn = attention(query, key, value, mask=mask,
                                 dropout=self.dropout)

        # 3) "Concat" using a view and apply a final linear.
        x = x.transpose(1, 2).contiguous() \
            .view(nbatches, -1, self.h * self.d_k)
        return self.linears[-1](x)


class PositionwiseFeedForward(nn.Module):
    "Implements FFN equation."

    def __init__(self, d_model, d_ff, dropout=0.1):
        super(PositionwiseFeedForward, self).__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        self.m=nn.GELU()
    def forward(self, x):
        return self.w_2(self.dropout(self.m(self.w_1(x))))


class Embeddings(nn.Module):
    def __init__(self, d_model, vocab):
        super(Embeddings, self).__init__()
        self.word_embedding = nn.Embedding(vocab, d_model)
        self.d_model = d_model
        self.position_embedding = PositionalEncoding(d_model, 0.1)

    def load_vocab(args):
        """Loads a vocabulary file into a dictionary."""
        vocab = collections.OrderedDict()
        index = 0
        vocab_file = '/content/drive/MyDrive/cjh/nmt/project3_nmt/my_vocab/my_vocab.txt'
        with open(vocab_file, "r", encoding="utf-8") as reader:
            while True:
                token = reader.readline()
                if not token:
                    break
                token = token.strip()
                vocab[token] = index
                index += 1
        return vocab

    def forward(self, x):
        return self.word_embedding(x) * math.sqrt(self.d_model) + self.position_embedding(x)
        #return self.word_embedding(x) + self.position_embedding(x)


class PositionalEncoding(nn.Module):
    "Implement the PE function."

    def __init__(self, d_model, dropout, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        # Compute the positional encodings once in log space.
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)
        # base = torch.ones(d_model//2).fill_(10000)
        # pow_term = torch.arnage(0, d_model, 2) / torch.tensor(d_model, dtype=torch.float32)
        # div_term = torch.pow(base, pow_term)
        div_term = torch.exp(torch.arange(0, d_model, 2) *
                             -(math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        pos = Variable(self.pe[:, :x.size(1)],
                       requires_grad=False)
        return self.dropout(pos)
