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

ambients=topology['plant']['ambients']

ambient=list(filter (lambda x:x['name'] == sys.argv[1],ambients))

lights=list(filter (lambda x:x['name'] == sys.argv[2],ambient[0]['modules']))

light_id=lights[0]['id']
print(light_id)

url="https://api.developer.legrand.com/hc/api/v1.0/"
url+="light/lighting/addressLocation/plants/"
url+=topology['plant']['id']
url+="/modules/parameter/id/value/"
url+=light_id

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': app_params['subscription_key'],
    'Authorization': authorization,
}

if (sys.argv[3] == "on"):
    data = '{"status": "on"}'
else:
    data = '{"status": "off"}'

response = requests.post(url, headers=headers, data=data)

print(response.text)


