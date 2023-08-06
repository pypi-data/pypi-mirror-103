import pandas as pd
import numpy as np
import tensorflow
import pathlib
import string
import keras
import re
import keras.backend as K
from keras.preprocessing.sequence import pad_sequences
from keras.engine.topology import Layer
from keras.models import load_model
from pythainlp.tag import pos_tag
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import download, get_corpus_path
from gensim.models import KeyedVectors

def load_embbed():
    HERE = pathlib.Path(__file__).parent

    download('thai2fit_wv')
    W_MODEL_PATH = get_corpus_path('thai2fit_wv')
    thai2fit_model = KeyedVectors.load_word2vec_format(W_MODEL_PATH,binary=True)
    thai2fit_weight = thai2fit_model.vectors
    thai2dict = {}   
    for word in thai2fit_model.index2word:
        thai2dict[word] = thai2fit_model[word]
    all_thai2dict = sorted(set(thai2dict))
    thai2dict_to_ix = dict((c, i) for i, c in enumerate(thai2dict)) #convert thai2fit to index 
    ix_to_thai2dict = dict((v,k) for k,v in thai2dict_to_ix.items())  #convert index to thai2fit
    print('')
    print('word2vec loaded')

    orchid_model = KeyedVectors.load(f'{HERE}/utility_data/postagging.wordvectors')
    listzero = [0]*50
    orchid_model.add('PAD',listzero)
    orchid_model.add('UNK',listzero)
    orchid_weight = orchid_model.vectors
    or2dict = {}   
    for word in orchid_model.index2word:
        or2dict[word] = orchid_model[word]
    all_or2dict = sorted(set(or2dict))
    or2dict_to_ix = dict((c, i+1) for i, c in enumerate(or2dict)) #convert orchid to index
    ix_to_or2dict = dict((v+1,k) for k,v in or2dict_to_ix.items())  #convert index to orchid
    print('orchid loaded')

    return thai2dict_to_ix, or2dict_to_ix, thai2dict, or2dict

def load_sentiment_model():
    HERE = pathlib.Path(__file__).parent

    loaded_sentiment_model = load_model(f'{HERE}/utility_data/BiGRU_best_weights.18-0.7049.hdf5', custom_objects={'SelfAttention': SelfAttention})
    print('model loaded')

    return loaded_sentiment_model

class SelfAttention(Layer):
    
    def __init__(self, **kwargs):
        
        super(SelfAttention,self).__init__()
        
    def build(self, input_shape):
        
        self.W=self.add_weight(name="att_weight", shape=(input_shape[-1],1), initializer="normal")
        self.b=self.add_weight(name="att_bias", shape=(input_shape[1],1), initializer="zeros")
        
        super(SelfAttention,self).build(input_shape)
        
    def call(self, x):
        
        e = K.tanh(K.dot(x,self.W)+self.b)
        a = K.softmax(e, axis=1)
        output = x*a

        return K.sum(output, axis=1)

    def get_config(self):

        config = super().get_config().copy()
        config.update({
            })

        return config

class Sentip():

    def __init__(self):
        self.thai2dict_to_ix, self.or2dict_to_ix, self.thai2dict, self.or2dict= load_embbed()
        self.loaded_sentiment_model = load_sentiment_model()

    def sentiment(self, inp):

        def clean_data_sen(sentence):
            sentence = sentence.lower()
            #clean all links, hashtags, tags, phone numbers
            sentence = re.sub(r"[@#]\S+|02\d{7}|0[689]\d{8}|http\S+|www\S+|m\.me\S+|\n","",sentence)
            sentence = re.sub(r"เเ",r"แ",sentence)
            #clean all special characters
            sentence  = "".join([char for char in sentence if char not in string.punctuation])

            return sentence

        def prepare_sequence_word(input_text):
            idxs = list()
            for word in input_text:
                if word in self.thai2dict:
                    idxs.append(self.thai2dict_to_ix[word])
                else:
                    #use unknown tag for unknown word
                    idxs.append(self.thai2dict_to_ix["unknown"]) 

            return idxs

        def prepare_tag_word(input_text):
            idxs = list()
            for word in input_text:
                if word in self.or2dict:
                    idxs.append(self.or2dict_to_ix[word])
                else:
                        #use UNK tag for unknown word
                    idxs.append(self.or2dict_to_ix["UNK"]) 

            return idxs

        def decode_label(pred):
            max_ind = np.argmax(pred)
            pred_dict = {0:'neg', 1:'neu', 2:'pos', 3:'q'}
            pred_de = pred_dict[max_ind]

            return pred_de

        if type(inp) == str:
            inp = np.array(inp)
            inp = inp.reshape(1)

        sentence = [clean_data_sen(x) for x in inp]
        sentence = [word_tokenize(x, engine="newmm", keep_whitespace=False) for x in sentence]
        word = [prepare_sequence_word(x) for x in sentence]
        word = pad_sequences(maxlen=450, sequences=word, 
                            value=self.thai2dict_to_ix["pad"], 
                            padding='post', truncating='post')
        word = word.reshape(len(inp),450)

        tag = [pos_tag(x, engine='perceptron', corpus='orchid') for x in sentence]
        static_tag = []
        for i in range(len(tag)):
            static_tag.append([tagtuple[1] for tagtuple in tag[i]])
        tag = [prepare_tag_word(x) for x in static_tag]
        tag = pad_sequences(maxlen=450, sequences=tag, 
                            value=self.or2dict_to_ix['PAD'], 
                            padding='post', truncating='post')
        tag = tag.reshape(len(inp),450)

        pred = self.loaded_sentiment_model.predict([word,tag])
        pred_de = [decode_label(x) for x in pred]

        return pred_de