#   Created by Anton Solovey, Falcongaze 2018 (c), a.solovey@falco3ngaze.ru

import json
import requests
from requests.auth import HTTPBasicAuth
import pprint

ST_IP = "http://192.168.50.22:"
ST_PORT = "9090"
CLIENT_ID = "custom_service"
CLIENT_HOST = "192.168.50.19"

def pretty(value, htchar='\t', lfchar='\n', indent=0):
    nlch = lfchar + htchar * (indent + 1)
    if type(value) is dict:
        items = [
            nlch + repr(key) + ': ' + pretty(value[key], htchar, lfchar, indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + lfchar + htchar * indent)
    elif type(value) is list:
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + lfchar + htchar * indent)
    elif type(value) is tuple:
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + lfchar + htchar * indent)
    else:
        return repr(value)

def print_json(data):           #   Function helper for pretty printing jsons. Not used now (using pprint instead) TODO: remove it
    if type(data) == dict:
        for k,v in data.items():
            print(k)
            print_json(v)
        else:
            print(data)

def server_register():      # User service register function

    register_url =  ST_IP + ST_PORT + "/api/v1/oauth2/register"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'client_id': CLIENT_ID, 'client_host': CLIENT_HOST}
    request = requests.post(register_url, headers=headers, data=payload)

    if request.status_code == 200:
        json_data = json.loads(request.content)
        return(json_data['secret_key'])
    else:
        print("Error: ", str(request.status_code), json.loads(request.content))

def get_oauth_token():
    
    token_url =  ST_IP + ST_PORT + "/api/v1/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'client_credentials', 'client_host': CLIENT_HOST}
    BASE64_CRED = HTTPBasicAuth(CLIENT_ID, server_register())
    request = requests.post(token_url, auth=BASE64_CRED, data=payload, headers=headers)

    if request.status_code == 200:
        json_data = json.loads(request.content)
        return(json_data['access_token'])
    else:
        print("Error: ", str(request.status_code), json.loads(request.content))

def get_usr_token():        # Auth internal ST user

    ST_INT_ADMIN = 'admin'
    ST_INT_ADMIN_PW = 'i5$(J|3a3_}6Ex)Y$Eezc&D^c8!77=m#0fnox$PnHMyC.Ft>p;B&H@B8k>u.t.;x'
    BASE64_CRED = HTTPBasicAuth(ST_INT_ADMIN, ST_INT_ADMIN_PW)
    
    usr_token_url = ST_IP + ST_PORT + "/api/v1/user/login"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'client_credentials'}

    request = requests.post(usr_token_url, auth=BASE64_CRED, headers=headers, data=payload)
    if request.status_code == 200:
        json_data = json.loads(request.content)
        return(json_data['access_token'])
    else:
        print("Error: ", str(request.status_code), json.loads(request.content))

def query_stats_request():
    search_url = ST_IP + ST_PORT + "/api/v1/search_requests/current"
    headers = {'Content-Type': "application/x-www-form-urlencoded",
               'Authorization': "Bearer " + get_usr_token(),
              }
    request = requests.get(search_url, headers=headers)

    if request.status_code == 200:
        pprint.pprint(json.loads(request.content), indent=3)
        #print_json(json.loads(request.content))
    else:
        print("Error: ", str(request.status_code), json.loads(request.content))

def search_request():
    search_url = ST_IP + ST_PORT + "/api/v1/data/collections/usbfiles/documents?offset=1516588172\&limit=10"
    headers = {'Content-Type': "application/x-www-form-urlencoded",
               'Authorization': "Bearer " + get_usr_token(),
               }
    print(search_url)
    request = requests.get(search_url, headers=headers)

    if request.status_code == 200:
        '''for item in request:
            print(item)'''
        pprint.pprint(json.loads(request.content), indent=3)
    else:
        print("Error: ", str(request.status_code), json.loads(request.content))

#   Main program

#search_request()
#query_stats_request()
#print(server_register())
#get_oauth_token()
#print(get_usr_token())
print('Server token: ', get_oauth_token())
