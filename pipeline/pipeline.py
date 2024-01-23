import threading
import logging
import time
from webex.integration import webexIntegration, webexLocal, webexService
from dateutil import tz
import datetime
import requests
import json
import concurrent.futures

log = logging.getLogger(__name__)
polling_interval = 360  # 3 minutes

# Wildcard * is supported by the API
# Example: MediaChannels.Call[1].Channel[1].Netstat.Bytes
# MediaChannels.*.Channel[1].Netstat.Bytes
# MediaChannels.*.Channel[1].Netstat.*
# MediaChannels.*.*.Netstat.*
# MediaChannels.*.*.Netstat.Bytes

# Metrics of interest
Metrics = ['SystemUnit.*',
           'Video.*',
           'Cameras.*',
           'Audio.*',
           'Network[*].*',
           'NetworkServices.NTP.*',
           'Time.*',
           'Peripherals.*',
           'Diagnostics.*',
           'RoomAnalytics.*',
           'Call[*].*']

xmlMetrics = ['*']


class DataPipeline():
    def __init__(self, client_id=None, client_secret=None,  username=None, password=None, access_token=None, refresh_token=None, redirect_uri=None, code=None, mode='Service', devices=[]):
        self.device = devices
        self.Data = []
        # Choose between Integration, Service or Local (On Premises) operation mode
        if mode == 'Service':
            self.webexGeter = webexService(
                client_id=client_id, client_secret=client_secret,  refresh_token=refresh_token, access_token=access_token)
        elif mode == 'Integration':
            self.webexGeter = webexIntegration(
                client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, code=code)
        else:
            self.webexGeter = webexLocal(
                username=username, password=password)
        # Run the pipeline
        self.__run()

    def __run(self):
        log.info('running pipeline...')
        # Max 150 threads working in parallel to avoid overloading the device
        with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
            while True:
                executor.map(self.sync_webex_xapi, self.device)
                time.sleep(polling_interval)

    def sync_webex_xapi(self, device):
        BRT = tz.gettz('America/Sao_Paulo')
        metrics = []
        for metric in Metrics:
            data = self.webexGeter.get_data_xapi(device, metric)
            # Check there is Call information and get the Netstat information
            if metric == 'Call[*].*' and 'result' in data:
                if data['result'] != {}:
                    t = self.webexGeter.get_data_xapi(
                        device, 'MediaChannels.*.*.Netstat.*')
                    if t != {} and 'result' in t:
                        data['result'].update(t['result'])
            try:
                metrics.append(
                    data['result'])
            except:
                pass

        try:
            # Post the data to ElasticSearch / Can be changed to any other database

            print(json.dumps({"@timestamp": str(datetime.datetime.now(
                tz=BRT).isoformat()), "Data": metrics, "DeviceId": device}))

            requests.post(url='http://localhost:9200/webexdata_device/_doc',  data=(json.dumps({"@timestamp": str(datetime.datetime.now(tz=BRT).isoformat()), "Data": metrics, "DeviceId": device})),
                          headers={'Content-type': 'application/json'}, auth=('admin', 'admin'), verify=False, timeout=10)

            log.info(
                f'Metrics sent to ElasticSearch Successfully for device {device}')

        except:
            log.error('Fail to contact ElasticSearch')
