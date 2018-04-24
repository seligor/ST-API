#   Created by Anton Solovey, Falcongaze 2018 (c), a.solovey@falcongaze.ru

import json
import requests
from requests.auth import HTTPBasicAuth

#   Here we define some default constants

ST_IP = "http://10.10.0.18:"
ST_PORT = "9090"
CLIENT_ID = "custom_service"
CLIENT_HOST = "10.10.200.2"

#   Classes

class st_auth:

    def server_register(self):      # User service register function

        register_url =  ST_IP + ST_PORT + "/api/v1/oauth2/register"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'client_id': CLIENT_ID, 'client_host': CLIENT_HOST}
        request = requests.post(register_url, headers=headers, data=payload)

        #   Check for HTTP 200 - if it's okay then return secret key
        if request.status_code == 200:
            json_data = json.loads(request.content)
            return(json_data['secret_key'])
        elif request.status_code == 409:    #   TODO:   check if server already registered then check token
            #raise Exception(json.loads(request.content))
            print("Already registered. ", "Error:", str(request.status_code), json.loads(request.content))
        elif request.status_code == 403:
            raise Exception("Registration rejected. " + json.loads(request.content))
        else:
            print("Error: ", str(request.status_code), json.loads(request.content))

    def get_oauth_token(self):

        token_url =  ST_IP + ST_PORT + "/api/v1/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'grant_type': 'client_credentials', 'client_host': CLIENT_HOST}
        BASE64_CRED = HTTPBasicAuth(CLIENT_ID, self.server_register())
        #   TODO:   check if token already exists then use that token
        request = requests.post(token_url, auth=BASE64_CRED, data=payload, headers=headers)

        
        if request.status_code == 401:      #   Check for token expire
            json_data = json.loads(request.content)
            print(json_data['code'])
        elif request.status_code == 200:    #   Check for HTTP 200 - if it's okay then return JWT token
            json_data = json.loads(request.content)
            return(json_data['access_token'])
        else:
            print("Error: ", str(request.status_code), json.loads(request.content))

    def request(self, token, resource_uri, http_method, http_payload=""):
        request_url = ST_IP + ST_PORT + resource_uri
        headers = {'Content-Type': "application/x-www-form-urlencoded",
               'Authorization': "Bearer " + token,
               }

        if http_method == "GET":
            request = requests.get(request_url, headers=headers)
        elif http_method == "POST":
            request = requests.post(request_url, headers=headers, data=http_payload)
        else:
            raise Exception("HTTP method is not implemented")

        if request.status_code == 200:
            '''for item in request:
                print(item)'''
            print(json.loads(request.content), indent=3)
        else:
            print("Error: ", str(request.status_code), json.loads(request.content))
