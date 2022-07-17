import json
import requests
import sys
import elasticsearch
from elasticsearch import helpers

users = None

with open(sys.argv[1]) as f:
    users = json.load(f)

url = "https://eogdata.mines.edu:9200/user-list"

es = elasticsearch.Elasticsearch(['https://eogdata.mines.edu:9200'], verify_certs=False, basic_auth=('elastic', 'elasticpassword'))

body = ""

actions = [
  {
    "_index": "user-list",
    "_source": user
  }
  for user in users
]

helpers.bulk(es, actions)


#response = requests.get(url, auth = requests.auth.HTTPBasicAuth('elastic', 'elasticpassword'), verify=False)

#print(response.content)
