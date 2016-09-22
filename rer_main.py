from rules import rules
from rermymaxent import rermymaxent
import rer_feature_functions
import rer_metrics
import json
class rer_main():
	def get_relation(self,ner_result):

		history={}
		history["relations"]=[]
		history["rel_tags"]=[[]]
		history["tags"]=ner_result["tags"]
		history["wn"]=0
		wmap=[]
		wmap.append({"words":ner_result["words"]})
		supported_rel = ["price_query","feature_query","interest_intent","comparison","irrelevant"]#,"disagreement","agreement","greeting","acknowledgement"]
		func_obj = rer_feature_functions.RerFeatureFunctions()#, supported_tags)
		func_obj.set_wmap(wmap) 
		clf = rermymaxent([], func_obj,supported_rel, reg_lambda = 0.001, pic_file = "rer_all_data.p")
		r = rules()
		val1 = clf.classify(history)
		val2 = r.classify(ner_result["words"])
		if val2 != None:
			val = val2
		else:
			val = val1 
		result={}
		result["words"]=wmap[0]["words"]
		result["tag"]=history["tags"]  
		result["relation"]=val  
		return result

def compute():
    json_file = r"rer_all_data.json"
    pickle_file = r"rer_all_data.p"
    # ----------------------------------------------------------------
    
    TRAIN = 1 #int(raw_input("Enter 1 for Train, 0 to use pickeled file:  "))
    supported_tags = ["Org", "OS", "Version", "Family", "Price", "Phone", "Feature" ,"Other"]
    supported_rel = ["price_query","feature_query","interest_intent","comparison","irrelevant"]#,"disagreement","agreement","greeting","acknowledgement"]
    tag_set = {"Org": 0, "Other": 1}
    dims = 9
    trg_data_x = []
    trg_data_y = []
    trg_data = {'Org': [], 'Other': []}
    data = json.loads(open(json_file).read())['root']
    
    (rer_history_list, wmap) = rer_feature_functions.build_history(data[0:75], supported_tags)
    print "After build_history"
    func_obj = rer_feature_functions.RerFeatureFunctions()#, supported_tags)
    func_obj.set_wmap(wmap) 
    clf = rermymaxent(rer_history_list[1:1400], func_obj,supported_rel, reg_lambda = 0.001, pic_file = pickle_file)
    #print clf.model
    if TRAIN == 1:
       clf.train()

    r=rules()
    results= rer_feature_functions.test(clf, r, rer_history_list[1:200], wmap)
    expected = []
    predicted = []
    for result in results :
        expected.append(result['expected'])
        predicted.append(result['predicted'])
		
    met_obj = rer_metrics.rer_metrics(expected, predicted)
    metrics = met_obj.compute()
    print metrics

