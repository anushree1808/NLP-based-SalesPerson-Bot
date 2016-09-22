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
import numpy
import pickle
import datetime
import re
from nltk.corpus import stopwords
phones = ["phone", "phones", "smartphone", "smartphones", "mobile"]
org_list = ["microsoft","google","samsung","htc","sony","apple","micromax","blackberry","karbonn","lenovo","lg","motorola","moto","facebook","whatsapp","xiomi","xiaomi"]
date_list=["year","month","week","yesterday","years","months","tomorrow","today","weeks","day","days","date","when","time"]
family_list=["galaxy", "lumia", "g", "h", "x", "e", "nexus", "desire", "series", "s", "iphone", "xperia","note"]
os_list=["android", "ios", "windows", "symbian", "bada", "os", "blackberry", "firefox"]
version_list=["lollipop", "kitkat", "jellybean","honeycomb","gingerbread","icecream","sandwich"]
app_list=["temple", "run", "candy", "crush", "whatsapp", "zomato", "autoid", "unblock", "photosphere", "siri", "gmail", "youtube", "messenger"] 
month_list=["january","february","march","april","may","june","july","august","september","october","november","december"]
feature_list=["screen","size","dual","sim","camera","front","back","rear","touch-screen","touch","screen","AOSP","wifi","wi-fi","display","battery","memory","ram","mp"]
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees"]
size_list = ["inch", "cm", "inches", "cms", r'"', "''", "pixel", "px", "mega", "gb", "mb", "kb", "kilo", "giga", "mega-pixel" ]
punctuation_list = [",", ";", "'", ".", ":", "?", "'s", "''", "' '", "!"]
stop = stopwords.words('english')
class FeatureFunctions(object):
    def __init__(self, tag_list = None):
        self.wmap = {}
        self.flist = {} #[self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10, self.f11, self.f12, self.f13]
        self.fdict = {}
        for k, v in FeatureFunctions.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'f':
                    self.flist[k] = v # .append(v)
                    tag = k[1:].split("_")[0]
                    val = self.fdict.get(tag, [])
                    val.append(v)
                    self.fdict[tag] = val

        self.supported_tags = self.fdict.keys()        
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
        for t, f in self.fdict.items():
            if t == tag:
                for f1 in f:
                    feats.append(int(f1(self, xi, tag)))
            else:
                for f1 in f:
                    feats.append(0)
        return feats
        
        
    # feature functions 
    # Org Tags    
    def fOrg_1(self, x, y):
        try :
            if y=="Org" and self.wmap[x["wn"]]["words"][x["i"]+1].lower() in ["phone","phones","smartphone","smartphones"]:
                return 1
        except :
            return 0    
        return 0    
        
    def fOrg_2(self, x, y):
        try :   
            if y=="Org" and self.wmap[x["wn"]]["words"][x["i"]+1].lower() in ["launches", "launched" ,"released", "releases"]:
                return 1
        except :
            return 0
        return 0       
        
    def fOrg_3(self, x, y):
        if y=="Org" and self.wmap[x["wn"]]["words"][x["i"]].lower() in org_list:
            return 1
        return 0            

    '''def fOrg_4(self, x, y):
        if y=="Org" and x["tb"]=="*" and x["ta"]=="*":
            return 1
        return 0
    
    def fOrg_5(self, x, y):
        if y=="Org" and x["ta"]=="*":
            return 1
        return 0'''
    
    #Family tags
    def fFamily_1(self, x, y):
        if y=="Family" and self.wmap[x["wn"]]["words"][x["i"]].lower() in family_list:
            return 1
        return 0        
        
    def fFamily_2(self, x, y):
        if y=="Family" and x["tb"]=="Org":
            return 1
        return 0    

    '''def fFamily_3(self, x, y):
        if y=="Family" and (("i" or "I" and "buy") in self.wmap[x["wn"]]["words"]): 
            return 1
        return 0'''
    
    def fFamily_4(self, x, y):
        try:
            if y=="Family" and x["tb"]=="Org" and x["ta"]=="Other":
                return 1
        except:
            return 0
        return 0
        
    '''def fFamily_5(self, x, y):
        if y=="Family" and x["ta"]=="*":
            return 1
        return 0
        
    def fFamily_6(self, x, y):
        if y=="Family" and x["tb"]=="Other":
            return 1
        return 0'''
        
    #Version tags
    def fVersion_1(self, x, y):
        if y=="Version" and "version" in self.wmap[x["wn"]]["words"]:
            return 1
        return 0
        
    def fVersion_2(self, x, y):
        if y=="Version" and self.wmap[x["wn"]]["words"][x["i"]].lower() in version_list:
            return 1
        return 0
        
    def fVersion_3(self, x, y):
        m = re.match(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?',self.wmap[x["wn"]]["words"][x["i"]])
        if y=="Version" and m and x["tb"]=="Version":
            return 1
        return 0
    
    def fVersion_4(self, x, y):
        if y=="Version" and x["tb"]=="OS":
            return 1
        return 0
    
    def fVersion_5(self, x, y):
        if y=="Version" and x["ta"]=="Org":
            return 1
        return 0
        
    '''def fVersion_6(self, x, y):
        if y=="Version" and self.wmap[x["wn"]]["words"][x["i"]-1] in (os_list or family_list):
            return 1
        return 0'''

    def fVersion_6(self, x, y):
        if y=="Version" and x["tb"]=="Version":
            return 1
        return 0
        
    #Other tags
    #Model
    def fOther_1(self, x, y):
        if y=="Other" and x["tb"]=="Family" and x["ta"]=="Org":
            return 1
        return 0

    #Model
    def fOther_2(self, x, y):
        if y=="Other" and x["tb"]=="Other" and x["ta"]=="Family":
            return 1
        return 0
    
    #App
    def fOther_3(self, x, y):
        if y=="Other" and self.wmap[x["wn"]]["words"][x["i"]] in app_list:    
            return 1
        return 0
    #Date
    def fOther_4(self, x, y):
        if y=="Other" and self.wmap[x["wn"]]["words"][x["i"]] in date_list:
            return 1
        return 0    
    
    #Date
    def fOther_5(self, x, y):
        if  y=="Other":
            for m in month_list:
                if self.wmap[x["wn"]]["words"][x["i"]].lower() in m:
                    return 1
        return 0                
   
    #Date
    def fOther_6(self, x, y):
        try:
            if y=="Other" and self.wmap[x["wn"]]["words"][x["i"]-1].lower() in ["before","after"]:
                return 1
        except :
            return 0
        return 0    

    #Place
    def fOther_7(self, x, y):
        if y=="Other":
            for suffix in ["lore", "pur", "nagar", "bad", "stan", "india", "karnataka", "usa", "halli", "land", "ai"]:
                if suffix in self.wmap[x["wn"]]["words"][x["i"]].lower() :
                    return 1
        return 0 

    #Place
    def fOther_8(self, x, y):
        if y=="Other" and self.wmap[x["wn"]]["words"][x["i"]].lower() in ["home", "where", "country", "place" ,"city" ,"state", "online" ,"offline", "showroom"]:
            return 1
        return 0
        
    #App
    def fOther_9(self, x, y):  
        if y=="Other" and self.wmap[x["wn"]]["words"][x["i"]].lower() in ["apps", "app", "play", "store"]:
            return 1
        return 0    

    #App
    def fOther_10(self, x, y):  
        if y=="Other" and x["tb"]=="OS":
            return 1
        return 0 

    def fOther_11(self, x, y):
        if y=="Other" and self.wmap[x["wn"]]["words"][x["i"]].lower() in stop:
            return 1
        return 0

    def fOther_12(self, x, y):
        if y=="Other" and self.wmap[x["wn"]]["words"][x["i"]].lower() in punctuation_list:
            return 1
        return 0

    def fOther_12(self, x, y):
        if y=="Other" and x["ta"]=="Other" and x["tb"]=="Other":
            return 1
        return 0

    def fOther_13(self, x, y):
        try:
            if y=="Other" and x["tb"]=="Other" and x["ta"]=="*":
                return 1
        except:
            return 0
        return 0   

    #Price tags
    def fPrice_1(self, x, y):
        try:
            if y=="Price" and ("Rs".lower() or "Rs.".lower()) in self.wmap[x["wn"]]["words"][x["i"]].lower()  or ("rs" or "rs.") in self.wmap[x["wn"]]["words"][x["i"]-1].lower():
                return 1
        except :
                return 0
        return 0     
    
    def fPrice_2(self, x, y):
        try :
            if y=="Price" and ( self.wmap[x["wn"]]["words"][x["i"]-2].lower() in ("priced", "less",  "greater", "price") or  self.wmap[x["wn"]]["words"][x["i"]-1].lower() in ("under", "priced") ):
                return 1
        except :
            return 0
        return 0        
    
    def fPrice_3(self, x, y):
        m = re.match("(\d+)[Kk]",self.wmap[x["wn"]]["words"][x["i"]])
        if y=="Price" and m:        
            return 1
        return 0 
        
    def fPrice_4(self, x, y):
        if y=="Price" and "price" in self.wmap[x["wn"]]["words"] or "range" in self.wmap[x["wn"]]["words"]:
            return 1
        return 0
        
    def fPrice_5(self, x, y):
        try:
            if y=="Price" and ("dollars" or "$") in self.wmap[x["wn"]]["words"][x["i"]+1].lower() or ("dollars" or "$") in self.wmap[x["wn"]]["words"][x["i"]-1].lower():
                return 1
        except:        
            return 0
        return 0    
    
    def fPrice_6(self, x, y):
        m = re.match(r'[1-9](?:\d{0,2})(?:,\d{3})*(?:\.\d*[1-9])?|0?\.\d*[1-9]|0',self.wmap[x["wn"]]["words"][x["i"]])
        if y=="Price" and m:
            return 1
        return 0
        
    #OS tags
    def fOS_1(self, x, y):
        if y=="OS" and self.wmap[x["wn"]]["words"][x["i"]].lower() in os_list:
            return 1
        return 0    

    def fOS_2(self, x, y):
        try:
            if y=="OS" and self.wmap[x["wn"]]["words"][x["i"]-1].lower() in ["run", "runs", "have", "has", "in", "on" ,"having", "an", "with"]:
                return 1
        except:
            return 0
        return 0
            
    def fOS_3(self, x, y):
        try: 
            if y=="OS" and self.wmap[x["wn"]]["words"][x["i"]+1].lower() in ["phone","phones", "version", "smartphones", "smartphone"]:
                return 1
        except:
            return 0
        return 0 
        
    def fOS_4(self, x, y):
        if y=="OS" and self.wmap[x["wn"]]["words"][x["i"]].lower() in os_list:
            return 1
        return 0 

    def fOS_5(self, x, y):
        if y=="OS" and x["tb"]=="Other":
            return 1
        return 0

    def fOS_6(self, x, y): 
        if y=="OS" and x["tb"]=="Other" and x["ta"]=="Other":
            return 1
        return 0
   
    #Phone tags
    def fPhone_1(self, x, y):
        if y=="Phone" and self.wmap[x["wn"]]["words"][x["i"]].lower() in ["phones", "phone", "smartphone","smartphones"]:
            return 1
        return 0    

    def fPhone_2(self, x, y):
        if y=="Phone" and x["tb"] in ["Org", "Family", "OS", "Model"]:
            return 1
        return 0    

    def fPhone_3(self, x, y):
        if y=="Phone" and ("phone" or "phones") in self.wmap[x["wn"]]["words"]:
            return 1
        return 0

    def fPhone_4(self, x, y): 
        if y=="Phone" and x["tb"]=="OS":
            return 1
        return 0

    def fPhone_5(self, x, y):
        if y=="Phone" and x["tb"]=="Org":
            return 1
        return 0
        
    #Feature tags   
    def fFeature_1(self, x, y):
        if y=="Feature" and self.wmap[x["wn"]]["words"][x["i"]].lower() in feature_list:
            return 1
        return 0
    
    def fFeature_2(self, x, y):
        if y=="Feature" and x["tb"]=="Other":
            return 1
        return 0
        
    def fFeature_3(self, x, y):
        if y=="Feature" and x["ta"]=="Other" and x["tb"]=="Other":
            return 1
        return 0
        
    def fFeature_4(self, x, y):
        if y=="Feature" and x["tb"]=="Feature":
            return 1
        return 0
    
    def fFeature_5(self, x, y):
        if y=="Feature" and x["tb"]=="Feature" and x["ta"]=="Other":
            return 1
        return 0
        
    def fFeature_6(self, x, y):
        m = re.match(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?',self.wmap[x["wn"]]["words"][x["i"]])
        if y=="Feature" and m:
            return 1
        return 0

def build_history(data_list, supported_tags):
    history_list = [] # list of all histories
    words_map = {}
    count = 0
    count_list=[]
    index=0
    for data in data_list: # data is the inputs entered by a given student
        data1 = data['data']
        for rec in data1:
            updates = rec['updates']
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

            len_sent=len(words)
            if index==0:
                count_list.append(len_sent)
            else: 
                count_list.append(count_list[index-1]+len_sent)   
            index+=1    

            for i in range(len(updates)):
                history = {}
                history["i"] = i
                if i == 0:
                    history["ta"] = "*" # special tag
                    history["tb"] = "*" # special tag
                elif i == 1:
                    history["ta"] = "*" # special tag
                    history["tb"] = updates[i - 1]['tag']
                else:
                    history["ta"] = updates[i - 2]['tag'] 
                    history["tb"] = updates[i - 1]['tag']
                history["wn"] = count
                history_list.append((history, updates[i]['tag'], ))
            count += 1
    return (history_list, words_map, count_list)    



def test(clf, history_list, wmap):
    result = []
    for history in history_list:
        mymap = self.wmap[history[0]["wn"]]
        words = mymap['words']
        #tags = mymap['pos_tags']    
        index = history[0]["i"]
        val = clf.classify(history[0])
        result.append({'predicted': val, 'word': words[index], 'expected': history[1]})
    return result
if __name__ == "__main__":
    pass
    #----- REPLACE THESE PATHS FOR YOUR SYSTEM ---------------------
    '''json_file = r"all_data.json"
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
    
    (history_list, wmap, count_list) = build_history(data[0:70], supported_tags)

    print "After build_history"
    func_obj = FeatureFunctions()#, supported_tags)
    func_obj.set_wmap(wmap) 
    clf = MyMaxEnt(history_list, func_obj, reg_lambda = 0.001, pic_file = pickle_file)
    print clf.model
    if TRAIN == 1:
       clf.train()
    '''
    '''result = test(clf, history_list[-500:])
    count_correct=0
    for r in result:
        print r['word'], r['predicted'], r['expected']
        if r['predicted'] == r['expected']:
            count_correct+=1
    print count_correct                
    '''
    '''
    tagged_sentences = []
    predicted = []
    for num in range(1, 1300):
        h_list = history_list[count_list[num-1]+1:count_list[num]+1]
        tagged_sentence=[]
        sentence_words = wmap[num]["words"]
        path=Viterbi(sentence_words, clf, supported_tags, h_list)
        print path
        for index in range(len(sentence_words)):
            tagged_sentence.append(h_list[index][1])
        tagged_sentences.append(tagged_sentence)
        predicted.append(path)
    ner=ner_metrics.NerMetrics(tagged_sentences,predicted)
    metrics=ner.compute()
    print "Metrics", metrics
    ner.print_results()

'''