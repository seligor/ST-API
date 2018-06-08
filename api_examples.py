#   Created by Anton Solovey, Falcongaze 2018 (c), a.solovey@falcongaze.ru

import client
import pprint
#   Some const and variables
ST_IP = "localhost"
ST_PORT = "9090"
CLIENT_HOST = "localhost"   # "10.10.200.2"

auth = client.Auth()   #   Create an instance of class
search = client.Search()
pp = pprint.PrettyPrinter(indent=3)

#   First, we have to register out custom service on SecureTower server
secret_key = auth.server_register(ST_IP, ST_PORT, CLIENT_HOST)
print("Secret key: ", secret_key)

#   Second, we have to get the token
oauth_token = auth.get_oauth_token(ST_IP, ST_PORT, CLIENT_HOST, secret_key)
print("Your token is: ", oauth_token)

pp.pprint("Collections list: " + search.get_collections(ST_IP, ST_PORT, oauth_token))
pp.pprint("Collection data: " + search.collection_request(ST_IP, ST_PORT, oauth_token, 'ftp'))

#   Then we can make a requests with the token

# st.request(ST_IP, ST_PORT, oauth_token, '/data/collections/', 'GET')
# st.request(ST_IP, ST_PORT, oauth_token, '/data/collections/httpurls/', 'GET')

#   Also you can make a request and get the token this way
#   st.request(ST_IP, ST_PORT, st.get_oauth_token(ST_IP, ST_PORT, CLIENT_HOST), '/data/collections/usbfiles/documents?offset=1525651200\&limit=10', "GET")

#   Let's make some other requests

