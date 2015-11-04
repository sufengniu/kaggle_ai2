import csv

class :
	'''
	this class parse the text file
	input: 
	output:
	'''
	def parse(object):
		'''
		'''
	with open('training_set.tsv', 'rb') as csvfile:
		MyDict = csv.DictReader(csvfile, delimiter='\t', quotechar=' ')
		MyDict2 = {}
		for line in MyDict:
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
			MyDict2[ID] = {}
			MyDict2[ID]['question'] = QUESTION_WORD
			MyDict2[ID]['correctAnswer'] = CORRECTANSWER_WORD
			MyDict2[ID]['A'] = A_WORD
			MyDict2[ID]['B'] = B_WORD
			MyDict2[ID]['C'] = C_WORD
			MyDict2[ID]['D'] = D_WORD
		print MyDict2["101246"]["B"]




