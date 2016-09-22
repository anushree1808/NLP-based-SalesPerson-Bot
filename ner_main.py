import feature_functions
from MyViterbi import MyViterbi
from MyMaxEnt import MyMaxEnt
import ner_metrics
import json

class ner_main():
	def classify(self, clf, history_list, wmap):
	    result = []
	    for index in range(len(history_list)):
	        mymap = self.wmap[history_list[index][0]["wn"]]
	        words = mymap['words']   
	        index = history_list[index][0]["i"]
	        val = clf.classify(history_list[index][0])
	        history_list[index+1]["ta"] = history_list[index]["tb"]
	        history_list[index+1]["tb"] = val			
	    return history_list

	def get_tags(self,sentence):
		supported_tags = ["Org", "OS", "Version", "Family", "Price", "Phone", "Feature" ,"Other"]
		func_obj = feature_functions.FeatureFunctions()
		wordlist=[]
		words=sentence.split(" ")
		mywords=words
		for word in words:
			wordlist.append(word)
		wmap=[]
		wmap.append({"words":words})	
		func_obj.set_wmap(wmap) 
		clf = MyMaxEnt([], func_obj, reg_lambda = 0.001, pic_file = 'all_data.p')
		history_list=[]

		for i in range(len(words)):
			history = {}
			history["i"] = i
			if i == 0:
			    history["ta"] = "*" # special tag
			    history["tb"] = "*" # special tag
			elif i == 1:
			    history["ta"] = "*" # special tag
			    history["tb"] = ""
			else:
			    history["ta"] = "" 
			    history["tb"] = ""
			history["wn"] = 0
			history_list.append((history, '', ))

		for index in range(len(history_list)):
			mymap = wmap[history_list[index][0]["wn"]]
			index = history_list[index][0]["i"]
			val = clf.classify(history_list[index][0])
			if index != len(history_list)-1:
				history_list[index+1][0]["ta"] = history_list[index][0]["tb"]
				history_list[index+1][0]["tb"] = val
		vitObj=MyViterbi()
		path=vitObj.Viterbi(words, clf, supported_tags, history_list)
		ner_tag_result={"words":words,"tags":path}
		#print ner_tag_result
		return ner_tag_result

	def compute(self):
		json_file = r"all_data.json"
		pickle_file = r"all_data.p"
	    # ----------------------------------------------------------------
	    
		TRAIN = 1 #int(raw_input("Enter 1 for Train, 0 to use pickeled file:  "))
		supported_tags = ["Org", "OS", "Version", "Family", "Price", "Phone", "Feature" ,"Other"]
	    
		tag_set = {"Org": 0, "Other": 1}
		dims = 9
		trg_data_x = []
		trg_data_y = []
		trg_data = {'Org': [], 'Other': []}
		data = json.loads(open(json_file).read())['root']
	    
		(history_list, wmap, count_list) = feature_functions.build_history(data[1:40], supported_tags)

		print "After build_history"
		func_obj = feature_functions.FeatureFunctions()#, supported_tags)
		func_obj.set_wmap(wmap) 
		clf = MyMaxEnt(history_list, func_obj, reg_lambda = 0.001, pic_file = pickle_file)
		print clf.model
		if TRAIN == 1:
			clf.train()

	    #-----------To test MaxEnt Classifier-------------------------------------------------

		'''
		result = feature_functions.test(clf, history_list[-500:], wmap)
		count_correct=0
		for r in result:
			print r['word'], r['predicted'], r['expected']
			if r['predicted'] == r['expected']:
				count_correct+=1
		print count_correct                
		'''

		vitObj=MyViterbi()
	    #----------To perform tagging using MEMM----------------------------------------------
		tagged_sentences = []
		predicted = []
		count_iters=0
		num=1
		#ner_tag_result=[]
		#print "Start Viterbi"
		while count_iters <= 3:
			
			num+=1
			try:
				h_list = history_list[count_list[num-1]+1:count_list[num]+1]
				tagged_sentence=[]
				sentence_words = wmap[num]["words"]
				path=vitObj.Viterbi(sentence_words, clf, supported_tags, h_list)
				print path
				#ner_tag_result.append({"words":sentence_words,"tags":path})
				for index in range(len(sentence_words)):
					tagged_sentence.append(h_list[index][1])
				tagged_sentences.append(tagged_sentence)
				predicted.append(path)
				count_iters+=1
			except:
				continue
		#print ner_tag_result	
		ner=ner_metrics.NerMetrics(tagged_sentences,predicted)
		metrics=ner.compute()
		#ner.print_results()
		#print "Metrics", metrics	

		#return ner_tag_result
#n=ner_main()
#n.compute()		