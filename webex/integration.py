import requests
from urllib3.exceptions import HTTPError
import logging
import base64
import urllib3
import xmltodict
import os

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


WEBEX_CLOUD_URI = 'https://webexapis.com'
LOCAL_URL = '/getxml?location=/Status/'

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def sub(string, old, nw):
    indice = string.find(old)
    if indice != -1:
        new_string = string[:indice] + nw + string[indice + 1:]
        return new_string
    else:
        return string


class webexIntegration():
    def __init__(self, client_id, client_secret, redirect_uri, code) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = None
        self.access_token = None
        self.redirect_uri = redirect_uri
        self.code = code

    # Get token for Integration
    def get_token(self):
        grant_type = "authorization_code"

        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        data = {
            'grant_type': grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.code,
            'redirect_uri': self.redirect_uri
        }
        try:
            res = requests.post('https://webexapis.com/v1/access_token',
                                headers=headers, data=data)
            res_json = res.json()
            self.access_token = res_json['access_token']
            self.refresh_token = res_json['refresh_token']
            os.putenv("WEBEX_INTEGRATION_ACCESS_TOKEN", self.access_token)
            os.putenv("WEBEX_INTEGRATION_REFRESH_TOKEN", self.refresh_token)

            log.info('New Access token and Refresh token acquired')

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')

    # Get Refresh the tokens for Integration
    def refresh_token(self):
        grant_type = 'refresh_token'

        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        data = {
            'grant_type': grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        try:
            res = requests.post('https://webexapis.com/v1/access_token',
                                headers=headers, data=data)
            res_json = res.json()
            self.access_token = res_json['access_token']
            self.refresh_token = res_json['refresh_token']
            os.putenv("WEBEX_INTEGRATION_ACCESS_TOKEN", self.access_token)
            os.putenv("WEBEX_INTEGRATION_REFRESH_TOKEN", self.refresh_token)
            log.info('Access token and Refresh token Refreshed')

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'Error during refresh_token: {res_json}')

    # Get data from xapi
    def get_data_xapi(self, id, metric_name):
        headers = {
            'authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'}
        if (id):
            try:
                response = requests.get(
                    WEBEX_CLOUD_URI+'/v1/xapi/status?' + 'deviceId='+id+'&'+'name='+metric_name, headers=headers)
                log.info('HTTP Resquet to {} succefull '.format(
                    WEBEX_CLOUD_URI+'/v1/xapi/status?' + 'deviceId='+id+' & '+'name='+metric_name))
                return response.json()
            except HTTPError as http_err:
                log.error(f'HTTP error occurred: {http_err}')
                # If the error code is 401, refresh the token and try again
                if http_err.code == 401:
                    self.refresh_token()
                    return self.get_data(id, metric_name)
                else:
                    return {}
        else:
            log.error('Missing ID')
            return {}

    def get_data(self, endpoint, **kwargs):
        headers = {
            'authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'}
        args = ''
        # Create the query for the request
        # See a example on app.py
        if (kwargs):
            for key, value in kwargs.items():
                args += '&' + key + '=' + value
            args.replace('&', '?', 1)
        if (endpoint):
            try:
                if (endpoint == '/v1/meeting/qualities'):
                    response = requests.get(
                        'https://analytics.webexapis.com' + endpoint + args, headers=headers)
                    log.info('HTTP Resquet to {} succefull '.format(
                        'https://analytics.webexapis.com' + endpoint + args))
                    return response.json()
                else:
                    response = requests.get(
                        WEBEX_CLOUD_URI + endpoint + args, headers=headers)
                    log.info('HTTP Resquet to {} succefull '.format(
                        WEBEX_CLOUD_URI + endpoint + args))
                    return response.json()
            except HTTPError as http_err:
                log.error(f'HTTP error occurred: {http_err}')
                if http_err.code == 401:
                    self.refresh_token()
                    return self.get_data(endpoint, kwargs=kwargs)
                else:
                    return {}
        else:
            log.error('Missing endpoint')
            return {}


class webexService():
    def __init__(self, client_id, client_secret, refresh_token, access_token) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = access_token

    def refresh_token(self):
        grant_type = 'refresh_token'

        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        data = {
            'grant_type': grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        try:
            res = requests.post('https://webexapis.com/v1/access_token',
                                headers=headers, data=data)
            res_json = res.json()
            self.access_token = res_json['access_token']
            self.refresh_token = res_json['refresh_token']
            os.putenv("WEBEX_SERVICE_ACCESS_TOKEN", self.access_token)
            os.putenv("WEBEX_SERVICE_TOKEN", self.refresh_token)
            log.info('Access token and Refresh token Refreshed')

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'Error during refresh_token: {res_json}')

    def get_data_xapi(self, id, metric_name):  # xapi
        headers = {
            'authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'}
        if (id):
            try:
                response = requests.get(
                    WEBEX_CLOUD_URI+'/v1/xapi/status?' + 'deviceId='+id+'&'+'name='+metric_name, headers=headers)
                log.info('HTTP Resquet to {} succefull '.format(
                    WEBEX_CLOUD_URI+'/v1/xapi/status?' + 'deviceId='+id+'&'+'name='+metric_name))
                return response.json()
            except HTTPError as http_err:
                log.error(f'HTTP error occurred: {http_err}')
                if http_err.code == 401:
                    self.refresh_token()
                    return self.get_data(id, metric_name)
                else:
                    return {}
        else:
            log.error('Missing ID')
            return {}


# Use with Any Webex  API

    def get_data(self, endpoint, **kwargs):  # xapi
        headers = {
            'authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'}
        args = ''
        if (kwargs):
            for key, value in kwargs.items():
                args += '&' + key.replace('_', '') + '=' + value
            args = sub(args, '&', '?')
        if (endpoint):
            try:
                if (endpoint == '/v1/meeting/qualities'):
                    response = requests.get(
                        'https://analytics.webexapis.com' + endpoint + args, headers=headers)
                    log.info('HTTP Resquet to {} succefull '.format(
                        'https://analytics.webexapis.com' + endpoint + args))
                    return response.json()
                else:
                    response = requests.get(
                        WEBEX_CLOUD_URI + endpoint + args, headers=headers)
                    log.info('HTTP Resquet to {} succefull '.format(
                        WEBEX_CLOUD_URI + endpoint + args))
                    return response.json()
            except HTTPError as http_err:
                log.error(f'HTTP error occurred: {http_err}')
                if http_err.code == 401:
                    self.refresh_token()
                    return self.get_data(endpoint, kwargs=kwargs)
                else:
                    return {}
        else:
            log.error('Missing endpoint')
            return {}


class webexLocal():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.access_token = self.username+':'+self.password

    def get_data_xapi(self, ip, metric_name):

        headers = {
            'authorization': 'Basic ' + base64.b64encode(
                self.access_token.encode("utf-8")).decode("utf-8"),
        }
        if (ip):
            try:
                response = requests.get(
                    'https://'+ip+'/getxml?location=/Status/'+metric_name, headers=headers, verify=False)
                log.info('HTTP Resquet to {} succefull '.format(
                    'https://'+ip+'/getxml?location=/Status/'+metric_name))

                return xmltodict.parse(response.text)
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                return {}
        else:
            log.error('Missing ip')
            return {}
