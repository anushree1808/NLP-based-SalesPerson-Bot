import pymongo
from pymongo import MongoClient
import requests
import json
import os
import re
from backend import backend

service_url = "http://jnresearch.com/"
#service_url = "http://localhost:9999/"
upload_url = service_url + "upload_file"
prod_bigrams_url = service_url + "get_brand_product_bigrams"
spec_fields_url = service_url + "get_spec_fields"
spec_url = service_url + "get_spec"
products_url = service_url + "get_products1"

class qgen(object):
	def __init__(self):
		self.b = backend("55555", "g15")

	#price_query
	def product_given_price_less_than(self,brand,price):
   		json_whole = self.b.get_products(brand)
   		products = []
   		for d in json_whole:
   			if int(d["dummy_price"])<int(price):
   				products.append(d["product"])
   		return products

   	#price_query
	def product_given_price_range(self,brand,price1,price2):
   		json_whole = self.b.get_products(brand)
   		products = []
   		for d in json_whole:
   			if int(d["dummy_price"])>=int(price1) and int(d["dummy_price"])<=int(price2):
   				products.append(d["product"])
   		return products

   	#price_query
	def product_given_price_greater_than(self,brand,price):
   		json_whole = self.b.get_products(brand)
   		products = []
   		for d in json_whole:
   			if int(d["dummy_price"])>int(price):
   				products.append(d["product"])
   		return products

   	#price_query
	def min_price(self, brand):
		price = self.b.get_products(brand)
		prices = []
		products = []
		for i in price:
			prices.append(int(i["dummy_price"]))
		a = min(prices)
		for j in price:
			if int(j["dummy_price"]) == a:
				d = {j["product"]:j["dummy_price"]}
				products.append(d)
		return products

	#price_query
	def get_price(self, brand, product):
		price = self.b.get_products(brand,product)
		prices = []
		for i in price:
			prices.append(i["dummy_price"])
		return prices

	#interest_intent
	def is_available(self, brand, product):
		list = self.b.get_spec(brand, product)
		for i in list:
			if (i["value"].lower() == "available" or (i["value"].split("."))[0].lower() == "available" and i["field"].lower() == "status" and i["category"].lower() == "general"):
				print("yes")
				break
			else:
				continue
			print("no")

	#interest_intent
	def get_products(self, brand):
		product = json.loads(self.b.get_brand_product_bigrams_dict())
		products = product[brand]
		print(self.get_products.__name__)
		return products

	#feature_query
	def get_DualSIM(self, brand):
		list = self.b.get_spec(brand)
		dualsim = []
		for i in list:
			if ("dual sim" in i["product"].lower()):
				dualsim.append(i["product"])
		return dualsim

	#feature_query
	def get_colors(self,brand,product):
   		json_whole = self.b.get_spec(brand,product)
   		for d in json_whole:
   			if d["category"].lower()=="features" and d["field"].lower()=="colors":
   				result = d["value"]
   		return result

   	#feature_query
	def is_radio(self, brand, product):
		specs=self.b.get_spec(brand,product)
		radio = []
		for i in specs:
			if i["category"].lower() == "features" and i["field"].lower() == "radio":
				radio.append(i["value"].lower())
		return radio

	#feature_query
	def get_battery_life(self, brand, product):
		specs=self.b.get_spec(brand,product)
		for i in specs:
			if i["category"].lower() == "battery": 
				battery = i["value"].lower()
		return battery

	#feature_query
	def get_memory_specs(self,brand,product):
		specs=self.b.get_spec(brand,product)
		for i in specs:
			if i["category"].lower() == "memory" and i["field"].lower() == "card slot":
				memory = i["value"]
		return memory

	def numCheck(self, num):
		m = re.match("(\d+).*",num)
		if m :
			print(type(m.group(1)))
			return m.group(1)
		else :
			return 'n'

	def price_query(self,words,tags):
		sentence=(" ").join(words)
		brand=""
		product=""
		word_price=[]
		phrases = ["less", "below", "great","more", "between", "range", "cheapest", "least","lowest", "how", "what","show","get"]
		for i in range(len(tags)):
			if tags[i]=="Org":
				brand=words[i]
			elif tags[i]=="Family":	
				product+=words[i]
			elif tags[i]=="Version":	
				product+=words[i]
			elif tags[i]=="Price":
				word_price.append(i)

		num1 = 0
		num2 = 0
		flag = 0
		ret_result = {}
		for j in range(len(phrases)) :
			if phrases[j] in sentence.lower():
				if j==0 or j==1 :
					if(len(word_price)>0):
						for k in word_price :
							num = words[k]
							print(type(num))
							if(self.numCheck(num) != 'n'):
								num1 = int(num)
								print("List of products less than price :  ")
								ret_result["result"] = self.product_given_price_less_than(brand,num1)
								ret_result["type"] = "models"
								print(ret_result)
								flag = 1
								return ret_result

				elif j==2 or j==3 :
					if(len(word_price)>0):
						for k in word_price :
							num = words[k]
							if(self.numCheck(num) != 'n'):
								num1 = int(num)
								print("List of products greater than price :  ")
								ret_result["result"] =self.product_given_price_greater_than(brand,num1)
								ret_result["type"] = "models"
								print(ret_result)
								flag = 1
								return ret_result

				elif j==4 or j==5 :
					if(len(word_price)>1):
						for k in word_price :
							num = words[k]
							if num1== 0 and (numCheck(num)!= 'n'):
								num1 = int(num)
							elif(self.numCheck(num) != 'n'):
								num2 = int(num)
						if num1 >0 and num2 > 0:	
							print("List of products in the range of price :  ")
							ret_result["result"]=self.product_given_price_range(brand,num1,num2)
							ret_result["type"] = "models"
							print(ret_result)
							flag = 1
							return ret_result

				elif j==6 or j==7 or j==8 :
					print("List of cheapest products :  ")
					ret_result["result"]=self.min_price(brand)
					ret_result["type"] = "models_cost"
					print(ret_result)
					flag = 1
					return ret_result

				else:
					print("Price :  ")
					ret_result["result"]=self.get_price(brand,product)
					ret_result["type"] = "cost"
					print(ret_result)
					flag = 1
					return ret_result

		if flag == 0:
			ret_result["result"]=""
			ret_result["type"] = "no_result"
			print("No price value")
			print(ret_result)
			return ret_result

	def interest_intent(self,words,tags):
		sentence=(" ").join(words)
		brand=""
		product=""
		word_price=[]
		phrases = ["have","do","available","what","can","could","tell","get"]
		for i in range(len(tags)):
			if tags[i]=="Org":
				brand=words[i]
			elif tags[i]=="Family":	
				product+=words[i]
			elif tags[i]=="Version":	
				product+=words[i]
			elif tags[i]=="Price":
				word_price.append(i)

		flag = 0
		for j in range(len(phrases)) :
			if phrases[j] in sentence.lower():
				if j==0 or j==1 or j==2 :
					self.is_available(brand,product)
					flag = 1
					break

				elif j==3 or j==4 or j==5 or j==6 or j==7:
					print("List of products: ")
					print(self.get_products(brand))
					flag = 1
					break

		if flag == 0:
			print("No value retrieved")

	def feature_query(self,words,tags):
		sentence=(" ").join(words)
		brand=""
		product=""
		word_price=[]
		phrases = ["dual","two","dual-sim","dualsim","colors","colours","color","colour","radio","battery","life","battery-life","memory","space","capacity"]
		for i in range(len(tags)):
			if tags[i]=="Org":
				brand=words[i]
			elif tags[i]=="Family":	
				product+=words[i]
			elif tags[i]=="Version":	
				product+=words[i]
			elif tags[i]=="Price":
				word_price.append(i)

		flag = 0
		for j in range(len(phrases)) :
			if phrases[j] in sentence.lower():
				if j==0 or j==1 or j==2 or j==3:
					print("Products that have dual sim")
					print(self.get_DualSIM(brand))
					flag = 1
					break

				elif j==4 or j==5 or j==6 or j==7:
					print("Colors available: ")
					print(self.get_colors(brand,product))
					flag = 1
					break

				elif j==8:
					print(self.is_radio(brand,product))
					flag = 1
					break

				elif j==9 or j==10 or j==11:
					print("Battery life:")
					print(self.get_battery_life(brand,product))
					flag = 1
					break

				elif j==12 or j==13 or j==14:
					print("Memory capacity:")
					print(self.get_memory_specs(brand,product))
					flag = 1
					break

		if flag == 0:
			print("No value retrieved")
								
	def get_data(self, d):
	# run the code below from different systems - replace the pw and groups - use g100, g101, g102, g103
	#ner = NerClient("55555", "g100")
	#json_file = r""
		#obj = qgen()
		#data = [{"words":["Get","all","products","of","Acer"],"tags":["Other","Other","Other","Other","Org"],"rel":["interest_intent"]}]#json.loads(open(json_file).read())
		res = ""
		
		words = d["words"]
		tags = d["tags"]
		rel = d["relation"]

		if(rel=="price_query"):
			res = self.price_query(words,tags)
		elif(rel=="interest_intent"):
			self.interest_intent(words,tags)
		elif(rel=="feature_query"):
			self.feature_query(words,tags)
		return res
'''
obj = qgen()
#data = [{"words":["Get","all","products","of","Acer"],"tags":["Other","Other","Other","Other","Org"],"rel":["interest_intent"]}]
#json.loads(open(json_file).read())
data = [{"words":["what","is","the","cost", "of", "Samsung", "E1195"],"tags":["Other","Other","Other","Price","Other","Org","Family"],"rel":["price_query"]}]
res_got = obj.get_data(data)
print(res_got)
'''