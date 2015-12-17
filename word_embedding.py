# test on word2vec package

import os
import sys

reload(sys)

import random
import multiprocessing
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import numpy as np
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

class my_sentences(object):
	def __init__(self, dirname):
		self.dirname = dirname
	
	def __iter__(self):
		for fname in os.listdir(self.dirname):
			for line in open(os.path.join(self.dirname, fname)):
				yield line.split()

class model_train(object):
    """ word2vec """
    def __init__(self):
    	self.model = Word2Vec()

    def word2vec(self, sentences):
    	# ignore words less then 5 times, parallel threads to be 8, 100 neuron size (50 to 100)
    	self.model = Word2Vec(sentences, min_count=5, size=200, window=5, workers=8)
		#self.model.build_vocab()

    def train(self):
        pass

    def word2phrase(self):
        pass

    def accuracy(self):
		self.model.accuracy('data/questions-words.txt')

wiki = my_sentences('data/wikipedia_sci')
w2v_model = model_train()
w2v_model.word2vec(sentences)
w2v_model.accuracy()

# load pre-train model from GloVe


