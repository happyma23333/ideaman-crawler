import requests
import json

r = requests.get("https://opencitations.net/index/api/v1/metadata/" +
                 "10.1287/MNSC.2017.2906")
#print(r.text)
rJson = json.loads(r.text)
print(rJson)
result = rJson[0]
reference = ""
citation = ""
if (result.get('reference')):
    reference = result['reference']

references = reference.split("; ")

if (result.get('citation')):
    citation = result['citation']

citations = citation.split("; ")

print("references: ")
for re in references:
    print(re)

print("citations: ")
for ci in citations:
    print(ci)
