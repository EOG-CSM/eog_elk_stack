import json
import requests
import sys
import elasticsearch
import elasticsearch.client
from elasticsearch import helpers

users = None

with open(sys.argv[1]) as f:
    users = json.load(f)

full_users = []
for user in users:
    full_users.append(user)
    if "email" in user:
        user_email_id = user.copy()
        user_email_id["id"] = user_email_id["email"]
        full_users.append(user_email_id)

special_users = [
    "eognrt",
    "seavision",
    "embassy",
    "oceana",
    "student",
    "gfw",
    "irma",
    "cmatthieu",
    "oceanmind",
    "ausdod",
    "smarthub",
    "fimo",
    "khang",
    "adi_susanto",
    "bfar",
    "phlcg",
    "phlncwc",
    "ana.sequeria",
    "dws",
    "m.meekan",
    "carlos.duarte",
    "ana.sequeira",
    "imarpe"
]

for user_name in special_users:
    #user = {"id": user_name, "email": user_name}
    #full_users.append(user)
    pass

url = "https://eogdata.mines.edu:9200/user-list"

es = elasticsearch.Elasticsearch(['https://eogdata.mines.edu:9200'], verify_certs=False, basic_auth=('elastic', 'elasticpassword'))


index_client = elasticsearch.client.IndicesClient(es)
try:
    index_client.delete(index="user-list")
except:
    pass

actions = [
  {
    "_index": "user-list",
    "_source": user
  }
  for user in full_users
]

helpers.bulk(es, actions)

enrich_client = elasticsearch.client.EnrichClient(es)

match = {
        "indices": "user-list",
        "match_field": "id",
        "enrich_fields": ["email"]
}

enrich_client.put_policy(name="add_email", match=match)
enrich_client.execute_policy(name="add_email", wait_for_completion=True)

ingest_client = elasticsearch.client.IngestClient(es)

processors = [{"enrich": {
    "policy_name": "add_email",
    "field": "user.name",
    "target_field": "userinfo",
    "max_matches": "1"
    }}]

ingest_client.put_pipeline(id="add_email", description="Adds email to apache access", processors=processors)


#response = requests.get(url, auth = requests.auth.HTTPBasicAuth('elastic', 'elasticpassword'), verify=False)

#print(response.content)
