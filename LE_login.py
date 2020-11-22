#!/bin/python

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl, parse_qs
from pathlib import Path
import time
import requests
import webbrowser
import json

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Authentication successfull</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><p>Authentication successfull.</p>", "utf-8"))
        self.wfile.write(bytes("<p>You can now close this page.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        res = parse_qs(urlparse(self.path).query)
        code = res['code'][0]
        app_params = json.loads(open(str(Path.home())+'/.config/LightControl/app_params.json').read())
        files = {
		    'client_id': (None, app_params['client_id']),
		    'client_secret': (None, app_params['client_secret']),
		    'grant_type': (None, 'authorization_code'),
	        'code': (None, code), 
        }
        response = requests.post('https://partners-login.eliotbylegrand.com/token', files=files)
        token=json.loads(response.text)
        token_str=json.dumps(token, indent = 4, sort_keys=True)
        f = open(str(Path.home())+"/.config/LightControl/token.json", "w")
        f.write(token_str)
        f.close() 
 
def log_into_legrand():
    app_params = json.loads(open(str(Path.home())+'/.config/LightControl/app_params.json').read())
    
    hostName=app_params['host_name']
    hostPort=app_params['host_port']
    
    myServer = HTTPServer((hostName, hostPort), MyServer)
    print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))
    
    # Display login page in a browser
    authorize_url="https://partners-login.eliotbylegrand.com/authorize"
    authorize_url+="?client_id="+app_params['client_id']
    authorize_url+="&response_type=code"
    authorize_url+="&redirect_uri="+app_params['redirect_uri']
    webbrowser.open(authorize_url, new=2)
    print("Browser should open, if not go to " + authorize_url)
    
    try:
    	# Handle one request then exit
    	myServer.handle_request()
    except KeyboardInterrupt:
        print("Exit via keyboard interrupt");
        pass
    
    myServer.server_close()

log_into_legrand()

