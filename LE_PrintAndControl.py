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
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': app_params['subscription_key'],
    'Authorization': authorization,
}

response = requests.get(url, headers=headers)

plant=json.loads(response.text)

lightstat = {}
for light in plant['modules']['lights']:
    id = light['sender']['plant']['module']['id']
    lightstat[id] = {}
    lightstat[id]["status"] = light['status']
    if "level" in light:
        lightstat[id]["level"] = light["level"]

lights=[]
lightno=0
for ambient in topology["plant"]["ambients"]:
    if len(ambient["modules"]) > 0:
        print (ambient["name"])
        for module in ambient["modules"]:
            if module["device"] == "light":
                lights.append(module["id"])
                l = lightstat[module["id"]]
                dispstr = " " + chr(ord('a') + lightno) + " "
                lightno += 1
                if l["status"] == "on":
                    dispstr += "# "
                else:
                    dispstr += "- "
                dispstr += module["name"]
                if "level" in l:
                    dispstr += " (" + str(l["level"]) + ")"
                print (dispstr)

cmd = input("cmd> ");
for c in cmd:
    i = ord(c) - ord('a')
    if i > 0 and i < len(lights):
        light_id = lights[i]
        if lightstat[light_id]["status"] == "on":
            data = '{"status": "off"}'
        else:
            data = '{"status": "on"}'
        url="https://api.developer.legrand.com/hc/api/v1.0/"
        url+="light/lighting/addressLocation/plants/"
        url+=topology['plant']['id']
        url+="/modules/parameter/id/value/"
        url+=light_id
        
        response = requests.post(url, headers=headers, data=data)

sys.exit(len(cmd)==0)
