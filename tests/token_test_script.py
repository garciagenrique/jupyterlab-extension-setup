import requests
import jwt
import urllib3
from rucio.client import Client
from rucio.client.downloadclient import DownloadClient

urllib3.disable_warnings()

# Token issuer endpoint
token_endpoint = 'https://iam-escape.cloud.cnaf.infn.it/token'

# Set user, password and client credentials
client_id = ''
client_secret = ''
password = ''
user = ''

# Request parameters (password grant flow)
params = {
    'grant_type': 'password',
    'username': user,
    'password': password,
    'client_id': client_id,
    'client_secret': client_secret
}

# Send POST request to token issuer for access token
response = requests.post(token_endpoint, data=params)

# Check response status code
if response.status_code == 200:
    # Token request successful
    token_data = response.json()
    access_token = token_data['access_token']
    # Use access token as needed
    print('Access token:', access_token)
else:
    # Token request failed
    print('Token request failed with status code:', response.status_code)

# Prepare the request data
data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
    'subject_token': access_token,
    'scope': 'openid email profile',
    'audience': 'rucio'
}

# Make the POST request to the token endpoint to get refresh token
response = requests.post(token_endpoint, data=data)

# Check the response
if response.status_code == 200:
    # Success
    print('Refresh token obtained successfully:')
    print(response.json()['access_token'])
    refresh_token = response.json()['access_token']
else:
    # Error
    print('Failed to obtain refresh token')
    print(response.status_code, response.text)

jwt_payload = jwt.decode(refresh_token, options={"verify_signature": False})

print("-----TOKEN PAYLOAD-----")
print(jwt_payload)

print("-----RUCIO AUTH TEST-----")
headers = {'X-Rucio-Auth-Token': refresh_token}
response = requests.get(url=f'https://vre-rucio.cern.ch/accounts/whoami', headers=headers, verify=False)
print(response.text)

# store the token in plain text file
with open('token.txt', 'w') as f:
    f.write(refresh_token)

# Setup rucio client
rucio_client = Client() # get from local rucio.cfg file

# Perform some tests with Rucio
rucio_client.ping()

print(rucio_client.whoami())

print(rucio_client.list_scopes())
l = rucio_client.list_rses()
l = list(l)
print(l)

did="test:jhub-domenic-noexp.txt"
rse="CERN-EOS"
dest_path="/Users/dom/code/goseind/jhub-cern-test"
download_client = DownloadClient(client=rucio_client)
download_client.download_dids([{'did': did, 'base_dir': dest_path}])
