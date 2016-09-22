class rer_metrics(object):
    def __init__(self, expected, predicted):
        self.expected = expected #list of list
        self.predicted = predicted #list
        self.accuracy = 0.0
        self.precision = 0.0
        self.recall = 0.0
        self.metrics = {} # this will be of the form: {'tag': {'precision':..., 'recall':..., 'f1':...}}
        return

    def compute(self):
        accuracy = 0
        count = 0
        total = 0
        
        for i in range(len(self.expected)): # each sentence
            #for j in range(len(self.expected[i])): # each word in a sentence
			expect=""
			if(len(self.expected[i])>1):
				if(self.predicted[i] in self.expected[i]):
					expect = predicted
				else:
					expect = self.expected[i][0]
			else :
				expect = self.expected[i][0]
				
			predict = self.predicted[i]
			met = self.metrics.get(expect, {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'accuracy': 0.0, 'tp': 0.0, 'fp': 0.0, 'total': 0.0})
			if (expect == predict): # check exp == predicted
				count += 1
				met['tp'] += 1
			else:
				met1 = self.metrics.get(predict, {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'accuracy': 0.0, 'tp': 0.0, 'fp': 0.0, 'total': 0.0})
				met1['fp'] += 1
				self.metrics[predict] = met1
			total += 1
			met['total'] += 1
			self.metrics[expect] = met                
        accuracy = float(count) / total
        for k, v in self.metrics.items():
            try:
                v['accuracy'] = float(v['tp']) / v['total']
                v['recall'] = float(v['tp']) / v['total']
                #exp_neg = total - v['total'] # this is FP + TN for the given tag
                v['precision'] = float(v['tp']) / (v['tp'] + v['fp'])
                v['f1'] = 2.0 * (v['precision'] * v['recall']) / (v['precision'] + v['recall'])
            except:
                print "Possible div by zero error for: ", k, v
                continue

        self.metrics["overall"] = {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'accuracy': accuracy, 'tp': count, 'total': total}      
        return self.metrics
	'''
    def print_results(self):
        for i in range(len(self.expected)):
            print '-' * 10, self.expected[i], '-' * 10
            for j in range(len(self.expected[i])):
                print self.expected[i][j], self.predicted[i][j]

	   for i in range(len(self.expected)):
            sent = ' '.join([w['word'] for w in self.expected[i]])
            print '-' * 10, sent, '-' * 10
            #print "slen = ", len(self.expected[i]), "  rlen = ", len(self.predicted[i])
            for j in range(len(self.expected[i])):
                print self.expected[i][j]['tag'], self.predicted[i][j]
        
        return
	'''
        
