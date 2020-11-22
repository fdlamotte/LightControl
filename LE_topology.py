#!/bin/python

from pathlib import Path
import requests
import json
import sys

def renew_token():
    global token
    global app_params

    files = {
        'client_id': (None, app_params['client_id']),
        'client_secret': (None, app_params['client_secret']),
        'grant_type': (None, 'refresh_token'),
        'refresh_token': (None, token['refresh_token']),
    }
    
    response = requests.post('https://partners-login.eliotbylegrand.com/token', 
        files=files)
    
    token=json.loads(response.text)
    token_str=json.dumps(token, indent = 4, sort_keys=True)
    
    f = open(str(Path.home())+"/.config/LightControl/token.json", "w")
    f.write(token_str)
    f.close() 

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

url = 'https://api.developer.legrand.com/hc/api/v1.0/plants'
response = requests.get(url, headers=headers)

if not response.ok: 
    # maybe token has expired
    renew_token()
    headers['Authorization'] = "Bearer " + token['access_token']
    response = requests.get(url, headers=headers)
    if not response.ok:
        sys.exit(-1)

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


