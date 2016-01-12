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

class dir_sentences(object):
	def __init__(self, dirname):	
		self.dirname = dirname

	def __iter__(self):
		for filename in os.listdir(self.dirname):
			for line in open(os.path.join(self.dirname, filename)):
				yield line.split()

class w2v_model(object):
    """ word2vec, doc2vec """
    def __init__(self):
    	self.model = Word2Vec()

    def train(self, sentences):
    	# ignore words less then 5 times, parallel threads to be 8, 100 neuron size (50 to 100)	
		bigram_transformer = gensim.models.Phrases(sentences)
		self.model = Word2Vec(bigram_transformer[sentences], min_count=5, size=150, window=5, workers=8)
		self.model.save('models/mymodel')
		self.model.save_word2vec_format('models/vector')
		#self.model.init_sims(replace=True)
		#self.model.build_vocab()

    def ctrain(self, sentences):
		self.model = Word2Vec.load('models/mymodel')
		self.model.train(sentences)

    def accuracy(self):
		self.model.accuracy('data/questions-words.txt')

# merge wiki data with text8
wiki = dir_sentences('data/wikipedia_sci')
text8 = LineSentence('data/text8')

pre_model = w2v_model()
pre_model.train(text8)
pre_model.accuracy()

pre_model.ctrain(wiki)
pre_model.accuracy()



# load pre-train model from GloVe


