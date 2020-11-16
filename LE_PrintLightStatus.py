import requests
import json
import sys

f=open('app_params.json', "r")
app_params = json.loads(f.read())
f.close()

f=open('token.json', "r")
token = json.loads(f.read())
f.close()

f=open('topology.json', "r")
topology = json.loads(f.read())
f.close()

authorization="Bearer " + token['access_token']

url="https://api.developer.legrand.com/hc/api/v1.0/"
url+="plants/"
url+=topology['plant']['id']

headers = {
    'Ocp-Apim-Subscription-Key': app_params['subscription_key'],
    'Authorization': authorization,
}

response = requests.get(url, headers=headers)

plant=json.loads(response.text)

print(json.dumps(plant['modules']['lights'], indent = 4))


