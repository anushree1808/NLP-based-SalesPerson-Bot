'''
feature_functions.py
Implements the feature generation mechanism
Author: Anantharaman Narayana Iyer
Date: 21 Nov 2014

6th Dec: Org gazeteer added
7th Dec: 
'''
from nltk import sent_tokenize, word_tokenize
import nltk
import json
import numpy
import pickle
import datetime
import re
import sys
from rermymaxent import rermymaxent
#import MyViterbi 
from collections import defaultdict
from nltk.corpus import stopwords
#import ner_metrics
from rules import rules
feature_list=["screen","size","dual","sim","camera","front","back","rear","touch-screen","touch","screen","AOSP","wifi","wi-fi","display","battery","memory","ram","mp"]
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees"]
size_list = ["inch", "cm", "inches", "cms", r'"', "''", "pixel", "px", "mega", "gb", "mb", "kb", "kilo", "giga", "mega-pixel" ]
punctuation_list = [",", ";", "'", ".", ":", "?", "'s", "''", "' '", "!"]

price_query_list=["cheapest","between","priced","price","less","range","cost","more","than","starting", "under","below", "costs","bargain", "expense","expenses"]
comparison_list=["vs","compare"," compares"," compared","comparison","better","slower","faster","cheaper","bigger","good","best","same","or","and"]
interest_intent_list=["need","buy","show","sale","want","would like to","do","have","What is the","Which is the","looking"]
feature_query_list=["features","featured","have","available","built","comes","with","play","runs","free"]

stop = stopwords.words('english')
class RerFeatureFunctions(object):
    def __init__(self, tag_list = None):
        self.wmap = {}
        self.rlist = {} 
        self.rdict = {}
        for k, v in RerFeatureFunctions.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'r':
                    self.rlist[k] = v
                    tag = k[1:].split("_")[0]+"_"+k[1:].split("_")[1]
                    val = self.rdict.get(tag, [])
                    val.append(v)
                    self.rdict[tag] = val

        self.supported_relations = self.rdict.keys()  
        #print self.rdict
        return

    def set_wmap(self, wmap): # given a list of words sets wmap
        self.wmap=wmap
        return

    def check_list(self, clist, w):
        #return 0
        w1 = w.lower()
        for cl in clist:
            if w1 in cl:
                return 1
        return 0
    def evaluate(self, xi, tag):
        feats = []
        for t, f in self.rdict.items():
            if t == tag:
                for f1 in f:
                    feats.append(int(f1(self, xi, tag)))
            else:
                for f1 in f:
                    feats.append(0)
        return feats
        
    def rprice_query_1(self, x, y):
        if y=="feature_query":
            words=self.wmap[x["wn"]]["words"]
            for word in words:
                if word.lower() in price_query_list:
                    return 1
        return 0   

    def rprice_query_2(self, x, y):
        if y=="price_query":
            words=self.wmap[x["wn"]]["words"]
            for word in words:
                if word.lower() in currency_symbols:
                    return 1
        return 0    
    def rprice_query_3(self, x, y):
        if y=="price_query":
            tags=x["tags"]
            if "Price" in tags:
                return 1        
        return 0         

    def rfeauture_query_1(self, x, y):    
        if y=="feature_query":
            words=self.wmap[x["wn"]]["words"]
            for word in words:
                if word in feature_query_list:
                    return 1
        return 0

    def rfeauture_query_2(self, x, y):    
        if y=="feature_query":
            tags=x["tags"]
            if "Feature" in tags:
                return 1
        return 0 

    def rfeauture_query_3(self, x, y):    
        if y=="feature_query":
            words=self.wmap[x["wn"]]["words"]
            for word in words:
                if word in feature_list:
                    return 1
        return 0     


    def rcomparison_1(self, x, y):
        if y=="comparison":
            words=self.wmap[x["wn"]]["words"]
            for word in words:
                if c in comparison_list: 
                   return 1
        return 0
        
    def rcomparison_2(self, x, y):
        if y=="comparison":
            tags=x["tags"]
            count={}
            for tag in tags:
                count[tag]=count[tag].setdefault(tag,0)+1
            if count["OS"]>=2 or count["Org"] >=2 or count["Family"]>=2 or count["Version"]>=2:
                return 1        
        return 0    
                    
    def rinterest_intent_1(self, x, y):
        if y=="feature_query":
            sent=(" ").join(self.wmap[x["wn"]]["words"])
            for ele in interest_intent_list:
                if ele in sent:
                    return 1
        return 0

    def rinterest_intent_2(self, x, y):
        if y=="interest_intent":
            words=self.wmap[x["wn"]]["words"]
            if "available" in words:
                tags=x["tags"]
                for tag in tags:
                    if tag in ["Org","Phone","Family","Model"]:
                        return 1  
        return 0  

    def rinterest_intent_3(self, x, y):
        if y=="interest_intent":
            words=self.wmap[x["wn"]]["words"]
            for word in words:
                if word.lower() in ["like","want","need","buy"]:
                    return 1  
        return 0    
       
    def rirrelevant_1(self, x, y):
        if y=="irrelevant":
            tags=x["tags"]
            for t in tags:
                if 'Others' != t:
                    return 0
            return 1
        return 0  
    '''
    def rirrelevant_2(self, x, y):
        if y=="irrelevant":
            tags = x["rel_tags"]
            if "Others" in set(tags[0]) and len(set(tags[0]))==1:
                return 1
        return 0
    '''
    def rirrelevant_2(self, x, y):
        if y=="irrelevant" and len(x["rel_tags"])==0:
            return 1
        return 0 
       

def build_history(data_list, supported_tags):
    rer_history_list = [] # list of all histories
    words_map = {}
    count = 0
    count_list=[]
    index=0
    for data in data_list: # data is the inputs entered by a given student
        data1 = data['data']
        for rec in data1:
            updates = rec['updates']
            try:
                rels = rec['rels']
            except:
                rels=[{"irrelevant":"Other"}] 
            sent = rec['sentence']
            words = []
              
            for i in range(len(updates)):
                words.append(updates[i]['word'])
                #------------------------------------------------------------------------------------------------
                # NOTE: below code is a temporary hack to build the MAxEnt for just 2 tags - we will change this later
                if(updates[i]['tag'] == "Model"):
                    updates[i]['tag']="Version"
                elif(updates[i]['tag'] == "Size"):
                    updates[i]['tag']="Feature" 
                elif(updates[i]['tag'] not in supported_tags):
                    updates[i]['tag'] = "Other"    
                        
                #------------------------------------------------------------------------------------------------

            words_map[count] = {'words': words}#, 'pos_tags': nltk.pos_tag(words)}
            rer_history = {}
            if(rels):
                rer_history["relations"] = rels[0].keys()
                rer_history["rel_tags"] = rels[0].values()
            else:
                rer_history["relations"] = ["irrelevant"]
                rer_history["rel_tags"] = [["Others"]]
            rer_history["wn"] = count
            rer_history["tags"] = []
            for i in range(len(updates)):
                rer_history["tags"].append(updates[i]['tag'])
            rer_history_list.append(rer_history)
            count+=1
            #print rel_history_list
    return (rer_history_list, words_map) 



def test(clf, r,rer_history_list, wmap):
    result = []
    count_correct=0
    for history in rer_history_list:
        mymap = wmap[history["wn"]]
        words = mymap['words']    
        val1 = clf.classify(history)
        val2 = r.classify(words)
        #print "val1 : ",val1
        #print "val1 : ",val2
        if val2!=None:
            val=val2
        else:
            val=val1    
        result.append({'predicted': val, 'sentence': words, 'expected': history["relations"]})
        if val in history["relations"]:
            count_correct+=1
        #print '************************8'    
    #print "accuracy : ",float(count_correct)/len(rer_history_list)
    #print "length of list : ",len(rer_history_list)       
    return result
if __name__ == "__main__":
    pass    
    ''' 
    count_correct=0
    for r in result:
        print r['word'], r['predicted'], r['expected']
        if r['predicted'] == r['expected']:
            count_correct+=1
    print count_correct                
    '''