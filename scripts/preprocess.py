import csv
import mmap
import progressbar
import wikipedia

# import os
import subprocess





parseDict = {}


class preprocess(object):
	""" preprocess class apply load file and parsing """

	def __init__(self, input_file):
		self.readDict = {}	
		if input_file.endswith('.tsv'):		# tsv file
			self.parse_tsv(input_file)
		elif input_file.endswith('.xml'):	# wiki dump file (.xml)
			self.load_wiki(input_file)
		else:
			sys.exit("incorrect input file format, must be tsv (.tsv) and wikipedia dump files (.xml)")

	def load_wiki(self, input_file):
		""" read wiki pre-train file """
		print 'load wiki dump file (', input_file, ')...'
		
		# os.system('../utils/wikiextractor/WikiExtractor "%s"' % input_file)
		subprocess.call("../utils/wikiextractor/WikiExtractor.py " + input_file, shell=True)
		
		# self.wiki_parse()


	def parse_tsv(self, input_file):	
		""" read input tsv file and parse input file by \t.
			format each question as following:
			question id: use id to query each question contents
			question contents
			answer (A/B/C/D)
			selection A
			selection B
			selection C
			selection D
		"""	
		print 'load tsv input file (', input_file, ')...'
		with open(input_file, 'rb') as csvfile:
			self.readDict = csv.DictReader(csvfile, delimiter='\t', quotechar=' ')
			lineNum = sum(1 for line in self.readDict)	
			bar = progressbar.ProgressBar(maxval = lineNum, \
					widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()
			print 'load file done, parse the input'
			i = 0
			for line in self.readDict:
				bar.update(i+1)
				csv.DictReader(csvfile, delimiter='\t', quotechar=' ')		
				ID = line['id'].strip()
				QUESTION = line['question'].strip()
				QUESTION_WORD = QUESTION.split()
				CORRECTANSWER = line['correctAnswer'].strip()
				CORRECTANSWER_WORD = CORRECTANSWER.split()
				A = line['A'].strip()
				A_WORD = A.split()
				B = line['B'].strip()
				B_WORD = B.split()
				C = line['C'].strip()
				C_WORD = C.split()
				D = line['D'].strip()
				D_WORD = D.split()

				parseDict[ID] = {}
				parseDict[ID]['question'] = QUESTION_WORD
				parseDict[ID]['correctAnswer'] = CORRECTANSWER_WORD
				parseDict[ID]['A'] = A_WORD
				parseDict[ID]['B'] = B_WORD
				parseDict[ID]['C'] = C_WORD
				parseDict[ID]['D'] = D_WORD
			bar.finish()
		print 'parsing done'
		

# initial test

preprocess('../data/training_set.tsv')
preprocess('../data/wikipedia_sci/wiki_sample.xml')

