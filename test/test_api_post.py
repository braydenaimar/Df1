
import boto3
import requests
from requests_aws4auth import AWS4Auth
# Use 'pip install boto3 requests requests-aws4auth' to get these

region_name = 'ap-southeast-2' # or 'us-west-1' or whatever

# 12 decimal digits from your AWS login page
account_id = '123456789012'

# I've only found this in the sample code for other languages, e.g. JavaScript
# Services→Cognito→Manage Federated Identities→(your-id-pool)→Sample code
identity_pool_id = 'ap-southeast-2:fedcba98-7654-3210-1234-56789abcdef0'

# Create a new identity
boto3.setup_default_session(region_name = region_name)
identity_client = boto3.client('cognito-identity', region_name=region_name)
identity_response = identity_client.get_id(AccountId=account_id,
    IdentityPoolId=identity_pool_id)

# We normally wouldn't log this, but to illustrate:
identity_id = identity_response['IdentityId']
print ('identity_id:', identity_id) # good idea not to log this

# Get the identity's credentials
credentials_response = identity_client.get_credentials_for_identity(IdentityId=identity_id)
credentials = credentials_response['Credentials']
access_key_id = credentials['AccessKeyId']
secret_key = credentials['SecretKey']
service = 'execute-api'
session_token = credentials['SessionToken']
expiration = credentials['Expiration']
# Again, we normally wouldn't log this:
print ('access_key_id', access_key_id)
print ('secret_key', secret_key)
print ('session_token', session_token)
print ('expiration', expiration)
# The access_key_id will look something like 'AKIABC123DE456FG7890', similar to
# Services→IAM→Users→(AWS_USER_NAME)→Security credentials→Access key ID

# Get the authorisation object
auth = AWS4Auth(access_key_id, secret_key, region_name, service,
    session_token=session_token)
current_app['auth'] = auth
# Just an illustration again:
print ('auth: %(service)s(%(date)s) %(region)s:%(access_id)s' % auth.__dict__)

# We'll use that object to send a request to our app. This app doesn't
# exist in real life, though, so you'll need to edit the following quite
# heavily:

# Services→Cognito→Manage your User Pools→(your-user-pool)→Apps→App name
app_name = 'my-app-name'

api_path = 'dev/helloworld'
method = 'GET'
headers = {}
body = ''
url = 'https://%s.%s.%s.amazonaws.com/%s' % (app_name, service, region_name,
    api_path)
response = requests.request(method, url, auth=auth, data=body, headers=headers)
