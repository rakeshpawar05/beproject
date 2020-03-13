import xml.etree.ElementTree as ET
import re
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers,losses
from tensorflow.keras import models

from language import Language

class Model:
    def __init__(self):
        pass
    def build(self,dataset,hidden_size=128):
        self.l = Language(dataset)
        inputs = layers.Input(shape=(self.l.max_encoder_seq_length,self.l.num_encoder_tokens))
        x = layers.LSTM(hidden_size,return_sequences=True)(inputs)
        x = layers.Flatten()(x)
        x = layers.RepeatVector(self.l.max_decoder_seq_length)(x)
        x = layers.Dense(hidden_size,activation='tanh')(x)
        x = layers.LSTM(hidden_size,return_sequences=True)(x)
        x = layers.Dense(self.l.num_decoder_tokens,activation='softmax')(x)
        #print(x.shape)
        self.model = keras.Model(inputs,x)
        self.model.compile(optimizer='adam',loss=losses.categorical_crossentropy,metrics=['accuracy'])
    def train(self,epochs=100,bsize=100):
        self.model.fit(self.l.encoder_input_data,self.l.decoder_input_data,epochs=epochs,batch_size=bsize)
    def predict(self,s):
        e = self.l.encode_input(s)
        prediction = self.model.predict(e)
        ans = ""
        for p in prediction[0]:
            out = self.l.reverse_target_word_index[np.argmax(p)]
            if out != "_end" and out != "_start":
                if out[1:].isnumeric() and (int(out[1:])-1) < len(s.split()):
                    #print(out)
                    ans += s.split()[int(out[1:])-1]+" "
                else:
                    ans += str(out)+" "
    #             ans += str(out)+" "
    #    print(s,"\noutput: ",ans,"\n")
        return ans
    def save(self,name=""):
        self.model.save("model"+str(name)+".h5")
        import pickle
        with open("language"+str(name)+".pickle","wb") as fp:
            pickle.dump(self.l,fp)
    def load(self,name=""):
        import pickle
        self.model = models.load_model("model"+str(name)+".h5")
        with open("language"+str(name)+".pickle","rb") as fb:
            self.l = pickle.load(fb)


