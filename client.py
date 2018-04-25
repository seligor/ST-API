#   Created by Anton Solovey, Falcongaze 2018 (c), a.solovey@falcongaze.ru

import json
import requests
from requests.auth import HTTPBasicAuth

#   Here we define some default constants

CLIENT_ID = "custom_service"

#   Classes

class st_auth:

    def server_register(self, st_ip, st_port, client_host):      # User service register function

        register_url =  "http://" + st_ip + ":" + st_port + "/api/v1/oauth2/register"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'client_id': CLIENT_ID, 'client_host': client_host}
        request = requests.post(register_url, headers=headers, data=payload)

        #   Check for HTTP 200 - if it's okay then return secret key
        if request.status_code == 200:
            json_data = json.loads(request.content)
            return(json_data['secret_key'])
        else:
            return("Error: ", str(request.status_code), json.loads(request.content))

    def api_error_handler(self, http_error_code, int_error_code):
        # pass    #   TODO:   make API HTTP error codes and internal error codes handler
        if http_error_code == 401 and int_error_code == 5:
            return(st_api.ST_INT_API_ERRORS("5"))
        elif http_error_code = 401 and int_error_code == 13:
            return(st_api.ST_INT_API_ERRORS("13"))
        elif http_error_code = 401 and int_error_code == 14:
            return(st_api.ST_INT_API_ERRORS("14"))
        elif http_error_code == 401 and int_error_code == 15:
            return(st_api.ST_INT_API_ERRORS("15"))
        elif http_error_code == 403 and int_error_code == 7:
            return(st_api.ST_INT_API_ERRORS("7"))
        #   Otherwise print an error
        else: 
            if http_error_code not in st_api.HTTP_ERRORS and int_error_code not in st_api.ST_INT_API_ERRORS
            print("Unknown error: ", str(http_error_code), json.loads(int_error_code))

    def get_oauth_token(self, st_ip, st_port, client_host):

        token_url =  "http://" + st_ip + ":" + st_port + "/api/v1/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'grant_type': 'client_credentials', 'client_host': client_host}
        BASE64_CRED = HTTPBasicAuth(CLIENT_ID, self.server_register(st_ip, st_port, client_host))
        #   TODO:   check if token already exists then use that token
        request = requests.post(token_url, auth=BASE64_CRED, data=payload, headers=headers)

        if request.status_code == 200:    #   Check for HTTP 200 - if it's okay then return JWT token
            json_data = json.loads(request.content)
            return(json_data['access_token'])
        else:
            #print("Error: ", str(request.status_code), json.loads(request.content))
            print(self.api_error_handler(request.status_code, request.content))

    def request(self, st_ip, st_port, token, resource_uri, http_method, http_payload=None):
        request_url = "http://" + st_ip + ":" + st_port + resource_uri
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

class st_api:
    
    RESOURCES = {
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

    COLLECTIONS = {
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

    HTTP_ERRORS = {
        "304": "Not Modified",
        "400": "Bad request",
        "401": "Not authorized",
        "403": "Fordidden",
        "501": "Not implemented",
        "503": "Service unavailable",        
    }   #   Just FYI

    ST_INT_API_ERRORS = {
        "5": "NotAuthenticated. There is no header with bearer token or Basic not sucsessful.",
        "7": "AccessForbidden. There is no appropriate right on your token.",
        "11": "Invalid upload rule. Database not exits OR rotation group not exists.",
        "13": "UserTokenInvalid. Token type is not supported.",
        "14": "UserTokenExpired. Token has been expired.",
        "15": "UserTokenInvalidSignature. Token digital signature is not valid.",
    }