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
        else:
            return("Error: ", str(request.status_code), json.loads(request.content))

    def api_error_handler(self):
        pass    #   TODO:   make API HTTP error codes and internal error codes handler

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

class st_api_methods:
    
    RESOURCES = 
    {
        "collections": "/data/collections",

        "consoles_versions": "/services/update",
        "client_console_version": "/services/update/client_console",
        "admin_console_version": "/services/update/admin_console",

        #   STATICTICS
        "current_search_queries": "/search_requests/current",
        "current_fulltext_queries": "/search_requests/current/ft",
        "current_dict_queries": "/search_requests/current/dict",
        "current_dfp_queries": "/search_requests/current/dfp",
        
        #   OTHER
        "upload": "/upload/",   # + name of collection
    }

    COLLECTIONS = 
    {
        "smtp": "smtp",
        "pop3": "pop3",
        "imap": "imap",
        "mapi": "mapi",
        "ftp": "ftp",
        "httpurls": "httpurls",
        "httpreq": "httpreq",
        "mailproc": "mailproc",
        "printer": "printer",
        "desktop": "desktop",
        "clipboard": "clipboard",
        "screenshots": "screenshots",
        "browsers": "browsers",
        "keylogger": "keylogger",
        "devices": "devices",
        "sharedfiles": "sharedfiles",
        "cddvd": "cddvd",
        "usbfiles": "usbfiles",
        "cloudfiles": "cloudfiles",
        "wsindexer": "wsindexer",
        "webmsg": "webmsg",
        "conversations": "conversations",      
    }

    HTTP_ERRORS = 
    {
        "304": "Not Modified",
        "400": "Bad request",
        "401": "Not authorized",
        "403": "Fordidden",
        "501": "Not implemented",
        "503": "Service unavailable",        
    }

    ST_INT_API_ERRORS =
    {
        "5": "NotAuthenticated",            #   There is no header with bearer token or Basic not sucsessful
        "7": "AccessForbidden",             #   There is no appropriate right on your token
        "11": "Invalid upload rule",        #   Database not exits OR rotation group not exists
        "13": "UserTokenInvalid",           #   Token type is not supported
        "14": "UserTokenExpired",           #   Token has been expired
        "15": "UserTokenInvalidSignature",  #   Token digital signature is not valid
    }