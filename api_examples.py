#   Created by Anton Solovey, Falcongaze 2018 (c), a.solovey@falcongaze.ru

import client

#   Some const and variables
ST_IP = "10.10.0.18"
ST_PORT = "9090"

st = client.st_auth()   #   Create an instance of class

#   First, we have to register our python client on SecureTower Storage as user service (as "custom_service")
st.server_register()    #   Try to register on ST Server
#   Next step we have to get token for our registered client
token = st.get_oauth_token()
#   After that we can make HTTP requests to SecureTower Server
st.request(ST_IP, ST_PORT, st.get_oauth_token(), '/api/v1/data/collections/usbfiles/documents?offset=1516588172\&limit=10', "GET")