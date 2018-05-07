#   Created by Anton Solovey, Falcongaze 2018 (c), a.solovey@falcongaze.ru

import client
#   Some const and variables
ST_IP = "192.168.50.22"
ST_PORT = "9090"
CLIENT_HOST = "192.168.50.19"   # "10.10.200.2"

st = client.securetower()   #   Create an instance of class

#   First, we have to register out custom service on SecureTower server
secret_key = st.server_register(ST_IP, ST_PORT, CLIENT_HOST)
#   Second, we have to get the token
oauth_token = st.get_oauth_token(ST_IP, ST_PORT, CLIENT_HOST, secret_key)
print(oauth_token)

#   Then we can make a requests with the token
st.request(ST_IP, ST_PORT, oauth_token, '/data/collections/', 'GET')
st.request(ST_IP, ST_PORT, oauth_token, '/data/collections/httpurls/', 'GET')

#   Also you can make a request and get the token this way
#   st.request(ST_IP, ST_PORT, st.get_oauth_token(ST_IP, ST_PORT, CLIENT_HOST), '/data/collections/usbfiles/documents?offset=1525651200\&limit=10', "GET")

#   Let's make some other requests

