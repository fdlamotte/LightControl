from pathlib import Path
import requests
import json
import sys

f=open(str(Path.home())+'/.config/LightControl/app_params.json', "r")
app_params = json.loads(f.read())
f.close()

f=open(str(Path.home())+'/.config/LightControl/token.json', "r")
token = json.loads(f.read())
f.close()

f=open(str(Path.home())+'/.config/LightControl/topology.json', "r")
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

lights = {}
for light in plant['modules']['lights']:
    id = light['sender']['plant']['module']['id']
    lights[id] = {}
    lights[id]["status"] = light['status']
    if "level" in light:
        lights[id]["level"] = light["level"]

for ambient in topology["plant"]["ambients"]:
    if len(ambient["modules"]) > 0:
        print (ambient["name"])
        for module in ambient["modules"]:
            if module["device"] == "light":
                l = lights[module["id"]]
                dispstr = "  " 
                if l["status"] == "on":
                    dispstr += "# "
                else:
                    dispstr += "- "
                dispstr += module["name"]
                if "level" in l:
                    dispstr += " (" + str(l["level"]) + ")"
                print (dispstr)
                
