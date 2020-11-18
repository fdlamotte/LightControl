#!/bin/python

import requests
import simplejson as json
import sys

lightstat = None

def get_plant():
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

    if not response.ok:
        return None

    return json.loads(response.text)


def renew_token():
    global token

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
    
    f = open("token.json", "w")
    f.write(token_str)
    f.close() 


def set_light_status(light_id, new_status):
    url="https://api.developer.legrand.com/hc/api/v1.0/"
    url+="light/lighting/addressLocation/plants/"
    url+=topology['plant']['id']
    url+="/modules/parameter/id/value/"
    url+=light_id

    data = '{"status": "' + new_status + '"}'
        
    response = requests.post(url, headers=headers, data=data)

def build_lightstat():
    lightstat = {}

    for light in plant['modules']['lights']:
        id = light['sender']['plant']['module']['id']
        lightstat[id] = {}
        lightstat[id]["status"] = light['status']
        if "level" in light:
            lightstat[id]["level"] = light["level"]

    return lightstat

def build_lightlist():
    lights=[]

    for ambient in topology["plant"]["ambients"]:
        if len(ambient["modules"]) > 0:
            for module in ambient["modules"]:
                if module["device"] == "light":
                    lights.append(module["id"])

    return lights


def build_ambientlist():
    amb=[]

    for ambient in topology["plant"]["ambients"]:
        if len(ambient["modules"]) > 0:
            amb.append(ambient["id"])

    return amb
    
def print_status():
    global lightstat
    lightno = 0
    for ambient in topology["plant"]["ambients"]:
        if len(ambient["modules"]) > 0:
            print (ambient["name"])
            for module in ambient["modules"]:
                if module["device"] == "light":
                    dispstr = " " + chr(ord('a') + lightno) + " "
                    lightno += 1

                    if not lightstat is None:
                        l = lightstat[module["id"]]
                        if l["status"] == "on":
                            dispstr += "# "
                        else:
                            dispstr += "- "
                    else:
                        dispstr += "- "

                    dispstr += module["name"]

                    if (not lightstat is None) and "level" in l:
                        dispstr += " (" + str(l["level"]) + ")"

                    print (dispstr)

def rewind(steps):
    dispstr = ""
    for i in range(steps+1):
        dispstr+="\033[F"
    print (dispstr)

# First print topology to user
f=open('topology.json', "r")
topology = json.loads(f.read())
f.close()

print_status()


# opening app parameters
f=open('app_params.json', "r")
app_params = json.loads(f.read())
f.close()

f=open('token.json', "r")
token = json.loads(f.read())
f.close()

plant = get_plant()
if plant is None:
    renew_token()
    plant = get_plant()
    if plant is None:
        sys.exit(-1) 

lightstat = build_lightstat()

# building lists of lights and ambients for the execution of commands
lights=build_lightlist()
ambients=build_ambientlist()

rewind(len(lights) + len(ambients))
print_status()

cmd = input("cmd> ");
for c in cmd:
    i = ord(c) - ord('a')
    if i > 0 and i < len(lights):
        light_id = lights[i]
    if lightstat[light_id]["status"] == "on":
        set_light(light_id, "off")
    else:
        set_light(light_id, "off")
    

sys.exit(len(cmd)==0)
