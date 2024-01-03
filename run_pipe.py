from pipeline.pipeline import DataPipeline
from webex.integration import webexIntegration, webexLocal, webexService
import dotenv
from os import getenv


dotenv.load_dotenv()
# API MODE
mode = getenv('WEBEX_API_MODE')

# WEBEX SERVICE APP
client_id = getenv('WEBEX_SERVICE_CLIENT_ID')
client_secret = getenv('WEBEX_SERVICE_CLIENT_SECRET')
access_token = getenv('WEBEX_SERVICE_ACCESS_TOKEN')
refresh_token = getenv('WEBEX_SERVICE_REFRESH_TOKEN')

# WEBEX INTEGRATION

redirect_uri = getenv('WEBEX_INTEGRATION_REDIRECT_URI')
integration_client_id = getenv('WEBEX_INTEGRATION_CLIENT_ID')
integration_client_secret = getenv('WEBEX_INTEGRATION_CLIENT_SECRET')

# ON PREMISES
username = getenv('WEBEX_USERNAME')
password = getenv('WEBEX_PASSWORD')


# Choose between Integration or Service
# Webex = webexIntegration(
#     client_id=integration_client_id, client_secret=integration_client_secret, code='', redirect_uri=redirect_uri)

Webex = webexService(
    client_id, client_secret, refresh_token, access_token)


data = []
_Devices = []

# Get all devices on the organization
resp = Webex.get_data('/v1/devices')
try:
    if 'items' in resp:
        for i in resp['items']:
            _Devices.append(i['id'])
        pipeline = DataPipeline(client_id=client_id, client_secret=client_secret,
                                username=username, password=password, access_token=access_token, refresh_token=refresh_token, mode=mode, devices=_Devices)
    else:
        print(resp)
except Exception as error:
    print('Error: ', error)
