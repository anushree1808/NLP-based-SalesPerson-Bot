class rules():
    def __init__(self):
        self.disagreement_list = ["no","wrong","incorrent","may","dont"]
        self.agreement_list = ["yes","right","correct","agree","may",]
        self.acknowledgement_list = ["thank","helpful","kind","sweet","informative","awesome","suggestion","ideas","yes"]
        self.greeting_list = ["hi","hello","morning","day","night","afternoon","hey","bye","cya"]
        self.rule_names=["disagreement","agreement","greeting","acknowledgement"]
        self.len_di=len(self.disagreement_list)
        self.len_ag=len(self.agreement_list)
        self.len_ac=len(self.acknowledgement_list)
        self.len_gr=len(self.greeting_list)
        self.threshold=0

    def classify(self, sentence):
        rule_set=[self.ruleDisagreement_1(sentence),self.ruleAgreement_1(sentence),self.ruleGreeting_1(sentence),self.ruleAcknowledgement_1(sentence)]
        max_v=rule_set[0]
        max_item=self.rule_names[0]
        i=1
        while i < 4:
            if rule_set[i]>max_v:
                max_v=rule_set[i]
                max_item=self.rule_names[i]
            i+=1    
        if max_v >self.threshold:      
            return max_item         
        else:
            return None 

    def ruleDisagreement_1(self,sentence):
        count=0
        for word in sentence:
            if word.lower() in self.disagreement_list:
                count+=1

        return float(count)/self.len_di
        
    def ruleAgreement_1(self,sentence):
        count=0
        for word in sentence:
            if word.lower() in self.agreement_list:
                count+=1
        return float(count)/self.len_ag

    def ruleAcknowledgement_1(self,sentence):
        count=0
        for word in sentence:
            if word.lower() in self.acknowledgement_list:
                count+=1
        return float(count)/self.len_ac  

    def ruleGreeting_1(self,sentence):
        count=0
        for word in sentence:
            if word.lower() in self.greeting_list:
                count+=1
        return float(count)/self.len_gr  