from pathlib import Path
import requests
import json

f=open(str(Path.home())+'/.config/LightControl/app_params.json', "r")
app_params = json.loads(f.read())
f.close()

f=open(str(Path.home())+'/.config/LightControl/token.json', "r")
token = json.loads(f.read())
f.close()

authorization="Bearer " + token['access_token']

headers = {
    'Ocp-Apim-Subscription-Key': app_params['subscription_key'],
    'Authorization': authorization,
}

response = requests.get('https://api.developer.legrand.com/hc/api/v1.0/plants', headers=headers)

plant=json.loads(response.text)['plants'][0]

url="https://api.developer.legrand.com/hc/api/v1.0/"
url+="plants/"
url+=plant['id']
url+="/topology"

headers = {
    'Ocp-Apim-Subscription-Key': app_params['subscription_key'],
    'Authorization': authorization,
}

response = requests.get(url, headers=headers)

topology=json.loads(response.text)
print(json.dumps(topology, indent = 4))


