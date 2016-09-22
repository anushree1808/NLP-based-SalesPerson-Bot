from ner_main import ner_main
from rer_main import rer_main
from qgen import qgen
import sys
from nlg import nlg
no_querying_list=["disagreement","agreement","greeting","acknowledgement"]

ner_obj=ner_main()
rer_obj=rer_main()
q_obj=qgen()
nlg_obj=nlg()
print "Welcome to chat session"
print "Type q to quit"

while True:
	customer_input=raw_input("Me: ")
	if(customer_input=='q'):
		sys.exit()
	ner_result=ner_obj.get_tags(customer_input)
	rer_result=rer_obj.get_relation(ner_result)
	relation=rer_result["relation"]
	print rer_result
	if relation in no_querying_list:
		salesman_reply=nlg_obj.getReply("no-query",rer_result["words"],relation)
	else:
		query_result=q_obj.get_data(rer_result)
		print query_result
		salesman_reply=nlg_obj.getReply("query",query_result["result"],relation)
	print "sg15: ",salesman_reply	

