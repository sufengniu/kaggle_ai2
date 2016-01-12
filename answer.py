import random;
import os;

class AnswerMachine( object ):

    def __init__(self):
        self.qContent = {};
        self.ans_A = {};
        self.ans_B = {};
        self.ans_C = {};
        self.ans_D = {};
        self.ans = {};
        pass

    def question_parser(self, questionPath=os.getcwd()):
        questionF = open(questionPath+'/data/validation_set.tsv', 'r');
        counter = 1;
        for line in questionF:
            if counter > 1:
                parts = line.split('\t');
                qID = parts[0];
                self.qContent[qID] = parts[1];
                self.ans_A[qID] = parts[2];
                self.ans_B[qID] = parts[3];
                self.ans_C[qID] = parts[4];
                self.ans_D[qID] = parts[5];
            counter += 1;
        pass

    def bob(self):
        answers = ['A','B','C','D'];
        for ques in self.qContent:
            self.ans[ques] = random.choice(answers);
        self._answer_sheet('Bob',os.getcwd())
        pass

    def jane(self):
        pass

    def _answer_sheet(self,taker,answerPath):
        ansSheet = open(answerPath+'/' + taker+'_answer.csv', 'w');
        ansSheet.write('id,correctAnswer\n');
        for ques in self.qContent:
            ansSheet.write(ques+','+self.ans[ques]+'\n');
        ansSheet.close()


# Initial Test
kaggle = AnswerMachine()
kaggle.question_parser()
kaggle.bob()