import torch
import numpy as np
from torch import nn, optim
from torch.nn import functional as F
from transformers.models.bert.modeling_bert import (
    BertModel,
    BertPreTrainedModel
)

#https://github.com/bcaitech1/p3-mrc-team-ikyo/blob/main/code/model/QueryAttentionModel.py 활용


class BertForQuestionAnswering(BertPreTrainedModel):
    _keys_to_ignore_on_load_unexpected = [r"pooler"]

    def __init__(self, config):
        super().__init__(config) 
        self.bert = BertModel(config, add_pooling_layer=True)
        self.config = config
        self.query_layer = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
        self.key_layer = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
        self.value_layer = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
        self.gelu = nn.GELU()
        self.drop_out = nn.Dropout(0.7)
        self.classify_layer = nn.Linear(config.hidden_size, 2, bias=True)
        self.start_linear = nn.Linear(config.hidden_size, 1)
        self.end_linear = nn.Linear(config.hidden_size, 1)

        self.init_weights()

    def forward(self, input_ids=None, attention_mask=None, token_type_ids=None, position_ids=None, 
    head_mask=None, inputs_embeds=None, start_positions=None, end_positions=None, output_attentions=None, output_hidden_states=None, return_dict=None, question_type=None):
        outputs = self.bert(
                input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
                position_ids=position_ids,
                head_mask=head_mask,
                inputs_embeds=inputs_embeds,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
            )
        
        sequence_output = outputs[0] # (B * 256 * 1024)

        
        embedded_query = sequence_output 
        embedded_query = self.query_layer(embedded_query) 
        embedded_query = torch.mean(embedded_query, 1, keepdim=True)
        embedded_key = self.key_layer(sequence_output)
        embedded_value = self.value_layer(sequence_output)

        attention_rate = torch.matmul(embedded_key, torch.transpose(embedded_query, 1, 2))
        attention_rate = F.softmax(attention_rate, 1) 

        logits = embedded_value * attention_rate 
        logits = self.gelu(logits)
        logits = self.drop_out(logits)
        logits = self.classify_layer(logits) 
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)

        return start_logits, end_logits 
    
    