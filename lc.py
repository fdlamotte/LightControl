#!/bin/python

import requests
try:
    import simplejson as json
except ImportError:
    import json
import sys
import time

lightstat = None

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
        rewind(1)
        print("Getting new token ...")
        renew_token()

        response = requests.get(url, headers=headers)
        if not response.ok:
            return None

    return json.loads(response.text)

def set_light(light_id, new_status):
    authorization="Bearer " + token['access_token']

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': app_params['subscription_key'],
        'Authorization': authorization,
    }

    url="https://api.developer.legrand.com/hc/api/v1.0/"
    url+="light/lighting/addressLocation/plants/"
    url+=topology['plant']['id']
    url+="/modules/parameter/id/value/"
    url+=light_id

    data = '{"status": "' + new_status + '"}'
        
    response = requests.post(url, headers=headers, data=data)

    if not response.ok:
        rewind(1)
        print("Getting new token ...")
        renew_token()
        response = requests.post(url, headers=headers, data=data)

def set_light_level(light_id, new_level):
    authorization="Bearer " + token['access_token']

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': app_params['subscription_key'],
        'Authorization': authorization,
    }

    url="https://api.developer.legrand.com/hc/api/v1.0/"
    url+="light/lighting/addressLocation/plants/"
    url+=topology['plant']['id']
    url+="/modules/parameter/id/value/"
    url+=light_id

    data = '{"level": ' + new_level + '}'
        
    response = requests.post(url, headers=headers, data=data)

    if not response.ok:
        rewind(1)
        print("Getting new token ...")
        renew_token()
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
                            dispstr += "\033[33m#\033[0m "
                        else:
                            dispstr += "\033[34m-\033[0m "
                    else:
                        dispstr += "- "

                    dispstr += module["name"]

                    if (not lightstat is None) and "level" in l:
                        dispstr += "\033[36m (" + str(l["level"]) + ")\033[0m"

                    print (dispstr)

def clear_line():
    sys.stdout.write(u"\u001b[0K")

def rewind(steps):
    for i in range(steps):
        sys.stdout.write(u"\u001b[0K\033[F")

def process_cmd(cmd):
    if cmd[0] >= 'A' and cmd[0] <= 'Z':
        # set the level of a light
        c = cmd[0]
        i = ord(c) - ord('A')
        set_light_level(lights[i], cmd[1:])
    else:
        # toggle each light in the string
        for c in cmd:
            if c >= 'a' and c <= 'z':
                i = ord(c) - ord('a')
                light_id = lights[i]
                if lightstat[light_id]["status"] == "on":
                    set_light(light_id, "off")
                else:
                    set_light(light_id, "on")

def cmd_loop():
    global lightstat
    global plant
    while True:
        rewind(len(lights) + len(ambients) + 1)
        print_status()
        clear_line()
        cmd = input("cmd> ");
        if len(cmd) > 0:
            process_cmd(cmd)
            time.sleep(0.5) # status update is not instantaneous
            plant=get_plant()
            lightstat=build_lightstat()
        else:
            break

# First print topology to user
f=open('topology.json', "r")
topology = json.loads(f.read())
f.close()

print_status()
print("Initializing ... ");

# opening app parameters
f=open('app_params.json', "r")
app_params = json.loads(f.read())
f.close()

f=open('token.json', "r")
token = json.loads(f.read())
f.close()

plant = get_plant()
if plant is None:
    sys.exit(-1)

lightstat = build_lightstat()

# building lists of lights and ambients for the execution of commands
lights=build_lightlist()
ambients=build_ambientlist()

cmd_loop()





