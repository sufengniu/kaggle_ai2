import csv
import mmap
import progressbar
import wikipedia
import fnmatch
# import os
import subprocess
import os.path

import get_wikipedia_data


parseDict = {}


class preprocess(object):
	""" preprocess class apply load file and parsing """

	def __init__(self, input_file):
		self.readDict = {}	
		if input_file.endswith('.tsv'):		# tsv file
			self.parse_tsv(input_file)
		#elif input_file.endswith('.xml'):	# wiki dump file (.xml)
		#	self.load_wiki(input_file)
		else:
			sys.exit("incorrect input file format, must be tsv (.tsv) and wikipedia dump files (.xml)")

		self.gen_wiki()

	'''
	def load_wiki(self, input_file):
		""" read wiki pre-train file """
		print 'load wiki dump file (', input_file, ')...'
		
		# os.system('utils/wikiextractor/WikiExtractor "%s"' % input_file)
		subprocess.call("utils/wikiextractor/WikiExtractor.py " + input_file, shell=True)
		
		# self.wiki_parse()
	'''

	def gen_wiki(self):
		print 'generating ck12 keywords list...'
		subprocess.call("./scrape.py > data/ck12_list_keywords.txt", shell=True)	
		print 'ck12 generating done, generating wiki plain text...'
		subprocess.call(["mkdir", "data/wikipedia_sci"])
		get_wikipedia_data.get_wikipedia_content_ck12_one_file_per_keyword('data/ck12_list_keywords.txt', 'data/wikipedia_sci')

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

	def parse_wiki(self,input_file):
		"""
		parse input file into two lists:
		plain text
		related word
		"""
		with open(input_file) as before_parsing:
			temp = before_parsing.read()
			refer_removed, sep, tail = temp.partition('== reference')
			if not sep:
				refer_removed, sep, tail = temp.partition('=== reference')
			ext_removed, sep, tail = refer_removed.partition('== external link')
			if not sep:
				ext_removed, sep, tail = refer_removed.partition('=== external link')
			main_contents, sep, relatedkeywords  = ext_removed.partition('== see also ==\n')
			if not sep:
				main_contents, sep, relatedkeywords  = ext_removed.partition('== see alsoedit ==')
			relatedkeywords, sep, tail  = relatedkeywords.partition('==')
			relatedkeyword = relatedkeywords.splitlines()

			main_contents = main_contents.splitlines()
			filtered = fnmatch.filter(main_contents,'=*=')
			plaintext = []
			for line in main_contents:
				if not any(filteredword in line for filteredword in filtered):
					plaintext.append(line)
				else:
					plaintext.append('\n')
			print 'parsing wiki done'

		def traverse_wikidata(wikidata, dir_name, files):
			'''
			traverse_wikidata
			function : traverse directory, parse wikipedia_txt_file 
			input : gained from calltraverse_wiki
			output : filename' '1' :[wiki plaintext] , '2' : [wiki_related_words]
			'''
			for line_main in files:
				with open(dir_name + '/' + line_main ) as before_parsing:
					temp = before_parsing.read()
					refer_removed, sep, tail = temp.partition('== reference')
					if not sep:
						refer_removed, sep, tail = temp.partition('=== reference')
					ext_removed, sep, tail = refer_removed.partition('== external link')
					if not sep:
						ext_removed, sep, tail = refer_removed.partition('=== external link')
					main_contents, sep, relatedkeywords  = ext_removed.partition('== see also ==\n')
					if not sep:
						main_contents, sep, relatedkeywords  = ext_removed.partition('== see alsoedit ==')
					relatedkeywords, sep, tail  = relatedkeywords.partition('==')
					relatedkeyword = relatedkeywords.splitlines()
					wikidata[line_main] = {}
					wikidata[line_main]['2'] = relatedkeyword
					main_contents = main_contents.splitlines()
					filtered = fnmatch.filter(main_contents,'=*=')
					plaintext = []
					for line in main_contents:
						if not any(filteredword in line for filteredword in filtered):
							plaintext.append(line)
						else:
							plaintext.append('\n')
					wikidata[line_main]['1'] = plaintext
			print 'parsing wiki txt done'

		def calltraverse_wiki(dir_name):
			'''
			call traverse_wiki
			input : wikipedia_txt_file_directory
			output : 'filename' '1' :[wiki plaintext] , '2' : [wiki_related_words]
			'''
			wikidata = { }
			os.path.walk(dir_name, traverse_wikidata, wikidata)



# initial test

preprocess('data/training_set.tsv')
#preprocess('data/wikipedia_sci/wiki_sample.xml')

