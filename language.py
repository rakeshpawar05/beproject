import xml.etree.ElementTree as ET
import re
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers,losses
from tensorflow.keras import models


class Language:
    def __init__(self,dataset):
        self.dataset,self.langdict = dataset
        self.input_lines = []
        self.target_lines = []
        self.input_words = set(["_end","_unk"])
        self.target_words = set(["_start","_end","_1","_2","_3","_4","_5","_6","_7","_8","_9","_10"])
        for line in self.dataset:
            input_text, target_text = line.split('\t')
            # We use "tab" as the "start sequence" wordacter
            # for the targets, and "\n" as "end sequence" wordacter.
            target_text = '_start ' + target_text + ' _end'
            self.input_lines.append(input_text)
            self.target_lines.append(target_text)
            for word in input_text.split():
                if word not in self.input_words:
                    self.input_words.add(word)
            for word in target_text.split():
                if word not in self.target_words:
                    self.target_words.add(word)

        self.input_words = sorted(list(self.input_words))
        self.input_words.remove("_unk")
        self.input_words.insert(0,"_unk")
        self.target_words = sorted(list(self.target_words))
        self.num_encoder_tokens = len(self.input_words)
        self.num_decoder_tokens = len(self.target_words)
        self.max_encoder_seq_length = max([len(txt.split()) for txt in self.input_lines])
        self.max_decoder_seq_length = max([len(txt.split()) for txt in self.target_lines])

        print('Number of samples:', len(self.input_lines))
        print('Number of unique input tokens:', self.num_encoder_tokens)
        print('Number of unique output tokens:', self.num_decoder_tokens)
        print('Max sequence length for inputs:', self.max_encoder_seq_length)
        print('Max sequence length for outputs:', self.max_decoder_seq_length)

        self.input_token_index = dict(
            [(word, i) for i, word in enumerate(self.input_words)])
        self.target_token_index = dict(
            [(word, i) for i, word in enumerate(self.target_words)])

        # dicts = (input_token_index,target_token_index,max_encoder_seq_length,num_encoder_tokens)

        # import pickle
        # with open("dicts.tuple","wb") as fp:
        #     pickle.dump(dicts,fp)

        self.reverse_input_word_index = dict(
            (i, word) for word, i in self.input_token_index.items())
        self.reverse_target_word_index = dict(
            (i, word) for word, i in self.target_token_index.items())

        self.encoder_input_data = np.zeros(
            (len(self.input_lines), self.max_encoder_seq_length, self.num_encoder_tokens),
            dtype='float32')
        self.decoder_input_data = np.zeros(
            (len(self.input_lines), self.max_decoder_seq_length, self.num_decoder_tokens),
            dtype='float32')
        self.decoder_target_data = np.zeros(
            (len(self.input_lines), self.max_decoder_seq_length, self.num_decoder_tokens),
            dtype='float32')

        for i, (input_text, target_text) in enumerate(zip(self.input_lines, self.target_lines)):
            for t, word in enumerate(input_text.split()):
                self.encoder_input_data[i, t, self.input_token_index[word]] = 1.
            self.encoder_input_data[i, t + 1:, self.input_token_index['_end']] = 1.
            for t, word in enumerate(target_text.split()):
                # decoder_target_data is ahead of decoder_input_data by one timestep
                self.decoder_input_data[i, t, self.target_token_index[word]] = 1.
                if t > 0:
                    # decoder_target_data will be ahead by one timestep
                    # and will not include the start wordacter.
                    self.decoder_target_data[i, t - 1, self.target_token_index[word]] = 1.
            self.decoder_input_data[i, t + 1:, self.target_token_index['_end']] = 1.
            self.decoder_target_data[i, t:, self.target_token_index['_end']] = 1.
    def encode_input(self,input_text):  
        encoder_input_data = np.zeros(
            (1, self.max_encoder_seq_length, self.num_encoder_tokens),
            dtype='float32')
        for t, word in enumerate(input_text.split()):
            if word in self.input_token_index.keys():
                encoder_input_data[0, t, self.input_token_index[word]] = 1.
            else:
                encoder_input_data[0, t, self.input_token_index["_unk"]] = 1.
        encoder_input_data[0, t + 1:, self.input_token_index['_end']] = 1.
        return encoder_input_data
