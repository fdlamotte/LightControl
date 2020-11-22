from pathlib import Path
import requests
import json

f=open(str(Path.home())+'/.config/LightControl/app_params.json', "r")
app_params = json.loads(f.read())
f.close()

f=open(str(Path.home())+'/.config/LightControl/token.json', "r")
token = json.loads(f.read())
f.close()

files = {
    'client_id': (None, app_params['client_id']),
    'client_secret': (None, app_params['client_secret']),
    'grant_type': (None, 'refresh_token'),
    'refresh_token': (None, token['refresh_token']),
}

response = requests.post('https://partners-login.eliotbylegrand.com/token', files=files)


token=json.loads(response.text)
token_str=json.dumps(token, indent = 4, sort_keys=True)

f = open(str(Path.home())+"/.config/LightControl/token.json", "w")
f.write(token_str)
f.close() 

