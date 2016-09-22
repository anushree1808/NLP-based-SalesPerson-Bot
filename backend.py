import pymongo
from pymongo import MongoClient
import requests
import json
import os

service_url = "http://jnresearch.com/"
#service_url = "http://localhost:9999/"
upload_url = service_url + "upload_file"
prod_bigrams_url = service_url + "get_brand_product_bigrams"
spec_fields_url = service_url + "get_spec_fields"
spec_url = service_url + "get_spec"
products_url = service_url + "get_products1"

class backend(object):
    def __init__(self, password, group):
        self.group = group
        self.password = password
        self.headers = {'content-type': 'application/json'}
        return

    def upload(self, fn):
        ret = upload_file(fn, self.password, self.group)
        return ret

    def get_brand_product_bigrams_dict(self):
        r = requests.post(prod_bigrams_url, data = json.dumps({"password": self.password, "group": self.group}), headers = self.headers) #
        return r.text


    def get_spec_fields(self):
        r = requests.post(spec_fields_url, data = json.dumps({"password": self.password, "group": self.group}), headers = self.headers) #
        print("returned")
        result = json.loads(r.text)
        return result

    def get_spec(self, brand, product = None):
        r = requests.post(spec_url, data = json.dumps({"password": self.password, "group": self.group, "brand": brand, "product": product}), headers = self.headers) #
        result = json.loads(r.text)
        return result

    def get_products(self, brand, product = None):
        r = requests.post(products_url, data = json.dumps({"password": self.password, "group": self.group, "brand": brand, "product": product}), headers = self.headers) #
        result = json.loads(r.text)
        return result

    def get_brand(self):
        brand_prod=json.loads(ner.get_brand_product_bigrams_dict())
        return brand_prod.keys()


if __name__ == "__main__":
    # run the code below from different systems - replace the pw and groups - use g100, g101, g102, g103
    ner = backend("55555", "g100")
    