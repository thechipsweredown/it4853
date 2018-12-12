import json
import requests

uri = "http://localhost:9200/dantri/_search"


def match_phrase(field,term):
    query = json.dumps({
        "from": 0, "size": 100,
        "query": {
            "match_phrase" : {
                field : term
            }
        }
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.get(uri, data=query,headers = headers)
    results = json.loads(response.text)
    return results['hits']

def match_phrase_prefix(fields,term):
    arr = []
    total = 0
    for f in fields:
        query = json.dumps({
            "from": 0, "size": 100,
            "query": {
            "match_phrase_prefix" : {
                f : {
                    "query" : term,
                    "max_expansions" : 10
                }
            }
        }})
        headers = {'Content-Type': 'application/json'}
        response = requests.get(uri, data=query,headers = headers)
        results = json.loads(response.text)['hits']
        for i in response["hits"]:
            for j in arr:
                if i["_id"] == j["_id"]:
                    continue
            arr.append(i)
            total += 1

        return json.dumps({
            "total" : total,
            "hits" : arr
        })


def matchMultifield(fields,term):
    query = json.dumps({

        "from": 0, "size": 100,
        "query": {
            "multi_match" : {
                "query": term,
                 "fields": fields,
                 "type": "phrase",
                 "slop": 3
        }
    }
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.get(uri, data=query,headers = headers)
    results = json.loads(response.text)
    return results['hits']

def searchField(fields,term):
    query = json.dumps({
        "from": 0, "size": 100,
        "query": {
            "multi_match" : {
            "query": term,
            "type": "most_fields",
            "fields" : fields
            }
        }
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.get(uri, data=query,headers = headers)
    results = json.loads(response.text)
    return results['hits']

def termQuery(term):
    query = json.dumps({
        "from": 0, "size": 100,
        "query": {
            "term" : { 
                "full_text" : term
                } 
        }
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.get(uri, data=query,headers = headers)
    results = json.loads(response.text)
    return results['hits']

def queryString(fields,term):
    query = json.dumps({
        "from": 0, "size": 100,
        "query": {
            "simple_query_string" : {
                "query": term,
                "fields": fields,
                "default_operator": "and"
            }
        }
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.get(uri, data=query,headers = headers)
    results = json.loads(response.text)
    return results['hits']

def querySuggest(term):
    data = []
    uri_suggest = "http://localhost:9200/title/_search?pretty"
    query = json.dumps({
        "suggest": {
        "key-suggest" : {
            "prefix" : term,
            "completion" : {
                "field" : "suggest"
                }
            }
        }
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.get(uri_suggest, data=query,headers = headers)
    results = json.loads(response.text)
    arrResults  = results['suggest']['key-suggest'][0]["options"]
    for j in arrResults:
        data.append(j["text"])

    return data


def format_results(results):
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        print("%s) %s" % (doc['_id'], doc['_source']['content']))