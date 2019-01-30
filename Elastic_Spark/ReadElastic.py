from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import NotFoundError
import json

es = Elasticsearch()

class_name = ["forest", "sea", "city", "mountain", "plan"]


for i in class_name:
    try:
        res = es.search(index="city", body={"query": {"match_all": {}}})

        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print("%(bucket)s: %(doc_id)s" % hit["_source"])

        
        print(res)
    except NotFoundError:
        pass
