#from urllib import response
from ast import arguments
from fileinput import filename
from matplotlib.font_manager import json_dump
import requests
import json
import sys, getopt
from collections import defaultdict

arg_list=sys.argv[1:]
options = "t:"

try:
    arguments, values = getopt.getopt(arg_list, options)
except getopt.error as err:
    print (str(err))
    sys.exit(2)

for arg, val in arguments:
    if arg == '-t':
        TOKEN = val
#print(TOKEN)

subid="5f2e9215-7c02-434e-bbf5-81bcfc0cec48"
rgname="FwSandbox"
policy="FwPolicy1"
apiversion="2023-02-01"

filename="idps_rules_list_3.json"
url = "https://management.azure.com/subscriptions/"+subid+"/resourceGroups/"+rgname+"/providers/Microsoft.Network/firewallPolicies/"+policy+"/listIdpsSignatures?api-version="+apiversion
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer '+TOKEN
}
payload = json.dumps({
  "search": "",
  "orderBy": {
    "field": "severity",
    "order": "Descending"
  },
  "resultsPerPage": 1000,
  "skip": 0
})
#allrules=defaultdict(list)
i=0

response = requests.request("POST", url, headers=headers, data=payload)
resp_dict= json.loads(response.text)
#print(resp_dict)
allrules=[]
allrules.extend(resp_dict['signatures'])
maxrule=resp_dict['matchingRecordsCount']
counter=(maxrule/1000)+1
print('matchingrecordcount:'+ str(maxrule))

#nextpage = 2
#print ("excuting api call to get all members")
while i < counter:
  print(i)
  i=i+1
  payload = json.dumps({
    "search": "",
    "orderBy": {
      "field": "severity",
      "order": "Ascending"
    },
    "resultsPerPage": 1000,
    "skip": (i*1000)
  })
  response = requests.request("POST", url, headers=headers, data=payload)
  resp_dict= json.loads(response.text)
  allrules.extend(resp_dict['signatures'])

# for rule in resp_dict['signature']:
#     #allrules[i]={}
    
#     allrules[i]['signatureId']=rule['signatureId']
#     allrules[i]['mode']=rule['mode']
#     allrules[i]['severity']=rule['severity']
#     allrules[i]['direction']=rule['direction']
#     allrules[i]['group']=rule['group']
#     allrules[i]['description']=rule['description']
#     allrules[i]['sourcePorts']=rule['sourcePorts']
#     allrules[i]['destinationPorts']=rule['destinationPorts']
#     allrules[i]['lastUpdated']=rule['lastUpdated']
#     allrules[i]['protocol']=rule['protocol']
#     allrules[i]['alertOnly']=rule['alertOnly']
#     i=i+1

#print(allrules)
print(len(allrules))
print(type(allrules))

with open (filename, 'w') as fp:
    json.dump(allrules, fp, indent=2) 