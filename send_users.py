import json
import requests
import sys
import elasticsearch
import elasticsearch.client
from elasticsearch import helpers

def send_users(es, filename):

    users = None
    
    with open(filename) as f:
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



def create_es():
    return elasticsearch.Elasticsearch(['https://eogdata.mines.edu:9200'], ca_certs='./ca.crt', basic_auth=('elastic', 'elasticpassword'))



def setup_pipelines(es):

    enrich_client = elasticsearch.client.EnrichClient(es)
    
    match = {
            "indices": "user-list",
            "match_field": "id",
            "enrich_fields": ["email"]
    }
    
    ingest_client = elasticsearch.client.IngestClient(es)
    
    
    try:
        ingest_client.delete_pipeline(id="my-apache-access-pipeline-main")
    except elasticsearch.NotFoundError:
        pass
    
    try:
        ingest_client.delete_pipeline(id="add_email")
    except elasticsearch.NotFoundError:
        pass
    
    try:
        enrich_client.delete_policy(name="add_email")
    except elasticsearch.NotFoundError:
        pass
    
    enrich_client.put_policy(name="add_email", match=match)
    enrich_client.execute_policy(name="add_email", wait_for_completion=True)
    
    
    processors = [{"enrich": {
        "policy_name": "add_email",
        "field": "user.name",
        "target_field": "userinfo",
        "max_matches": "1"
        }}]
    
    
    try:
        apache_ingest_id = list(ingest_client.get_pipeline(id="filebeat-*-apache-access-pipeline").body.keys())[0]
    except elasticsearch.NotFoundError:
        print("must run filebeat setup first")
        os.exit(1)
    
    ingest_client.put_pipeline(id="add_email", description="Adds email to apache access", processors=processors)
    
    
    main_pipeline_processors = [
        {
          "pipeline": {
            "description" : "Call the default apache access pipeline",
            "name": apache_ingest_id
          }
        },
        {
        "pipeline": {
          "description" : "Call my additional apache access pipeline",
          "name": "add_email"
        }
        }
    ]
    
    ingest_client.put_pipeline(id="my-apache-access-pipeline-main", description="Main apache pipeline.", processors=main_pipeline_processors)


def create_api_key(es):
    security = elasticsearch.client.SecurityClient(es)
    key = security.create_api_key(name="filebeat")
    return (f'{key.body["id"]}:{key.body["api_key"]}')

if __name__ == '__main__':
    if sys.argv[1] == 'api':
        print(create_api_key(create_es()))
    elif sys.argv[1] == 'setup':
        es = create_es()
        send_users(es, sys.argv[2])
        setup_pipelines(es)

