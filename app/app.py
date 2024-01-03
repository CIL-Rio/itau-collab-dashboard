from flask import Flask
from flask_cors import CORS
from http import HTTPStatus
from flask import jsonify, request, render_template
from pipeline.pipeline import DataPipeline
from webex.integration import webexIntegration, webexLocal, webexService
import dotenv
from os import getenv, putenv
from pipeline.data_dict import device
import requests
import datetime
from dateutil import tz
import json

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

BRT = tz.gettz('America/Sao_Paulo')

if mode == 'Integration':
    Webex = webexIntegration(
        client_id=integration_client_id, client_secret=integration_client_secret, code='', redirect_uri=redirect_uri)
else:
    Webex = webexService(
        client_id, client_secret, refresh_token, access_token)


def modify_nested_dict(dictionary, value):
    for key, val in dictionary.items():
        if isinstance(val, dict):
            modify_nested_dict(val, value)
        elif val == -1:
            dictionary[key] = value
    return dictionary


app = Flask(__name__, static_folder='../static',)
CORS(app)


@app.route('/', methods=['GET'])  # Integration Auth used
def webex_auth():
    code = request.args.get('code')
    putenv("WEBEX_INTEGRATION_CODE", code)

    return '<h1>Running mode: {} </h1> <br> Auth-code: {}</br>'.format(mode, code), HTTPStatus.OK


@app.route('/workspace-metrics/<workspaceId>', methods=['GET'])
@app.route('/workspace-metrics', methods=['GET'])
def workspaces_metrics():
    timeUsed = []
    timeBooked = []
    workspaceId = request.args.get('workspaceId')

    aggregation = 'daily'
    _from = '2023-09-12T09:00:00.000Z'
    to = '2023-09-12T22:00:00.000Z'

    if (request.args.get('aggregation')):
        aggregation = request.args.get('aggregation')
    if (request.args.get('from')):
        _from = request.args.get('from')
    if (request.args.get('to')):
        to = request.args.get('to')

    if workspaceId:
        timeUsed.append(Webex.get_data(
            '/v1/workspaceDurationMetrics', workspaceId=workspaceId, aggregation=aggregation, _from=_from, to=to, measurement='timeUsed'))

        timeBooked.append(Webex.get_data(
            '/v1/workspaceDurationMetrics', workspaceId=workspaceId, aaggregation=aggregation, _from=_from, to=to, measurement='timeBooked'))
    else:
        workspaces = Webex.get_data('/v1/workspaces')
        if workspaces['items']:
            for workspace in workspaces['items']:
                timeUsed = Webex.get_data(
                    '/v1/workspaceDurationMetrics', workspaceId=workspace['id'], aggregation=aggregation, _from=_from, to=to,  measurement='timeUsed')

                timeBooked = Webex.get_data(
                    '/v1/workspaceDurationMetrics', workspaceId=workspace['id'], aggregation=aggregation, _from=_from, to=to,  measurement='timeBooked')

    return jsonify({'timeUsed': timeUsed, 'timeBooked': timeBooked}), HTTPStatus.OK


@app.route('/meetings-metrics', methods=['GET'])
def meeting_metrics():
    meetingIds = []
    _from = '2023-09-12T09:00:00.000Z'
    to = '2023-09-12T22:00:00.000Z'
    siteUrl = 'lschwabd-ga-sandbox.webex.com'

    if (request.args.get('from')):
        _from = request.args.get('from')
    if (request.args.get('to')):
        to = request.args.get('to')
    if (request.args.get('siteUrl')):
        siteUrl = request.args.get('siteUrl')

    if (request.args.get('meetingId')):
        meetingIds.append(request.args.get('meetingId'))
    resp = Webex.get_data(
        '/v1/meetingReports/usage', siteUrl=siteUrl, _from=_from, to=to)
    qualities = []
    if resp['items']:
        for meeting in resp['items']:
            qualities = Webex.get_data(
                '/v1/meeting/qualities', meetingId=meeting['meetingId'])
            for quality in qualities['items']:
                if quality["clientType"] == "TEAMS_DEVICE":
                    print(quality['audioOut'][0]['packetLoss'])
                    data = {"@timestamp": str(datetime.datetime.now(tz=BRT).isoformat()), "Data": {
                        'QualityMetrics': quality}, "meetingID": meeting['meetingId']}
                    r = requests.post(url='http://localhost:9200/webexdata_meeting_metrics/_doc', data=json.dumps(data),
                                      headers={'Content-type': 'application/json'}, auth=('admin', 'admin'), verify=False)
            print(r.status_code, r.json())
    return jsonify({'QualityMetrics': qualities}), HTTPStatus.OK
