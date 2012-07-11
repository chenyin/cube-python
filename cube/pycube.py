import requests
from datetime import datetime
import json

CUBE_SECOND = "1e4" #- 10-second
CUBE_MINUTE = "6e4" #- 1-minute
CUBE_FIVE_MINUTE = "3e5" #- 5-minute
CUBE_HOUR = "36e5" #- 1-hour
CUBE_DAY = "864e5" #- 1-day

class CubeEvent(object):
    def __init__(self, etype, edata, etime):
        self.etype = etype
        self.edata = edata
        self.etime = etime

    def to_json(self):
        d = {}
        d['type'] = self.etype
        d['time'] = self.etime
        d['data'] = self.edata
        return d

def to_jsons(ces):
    if type(ces) is not list:
        ces = [ces, ]
    return json.dumps([ce.to_json() for ce in ces])


DEFAULT_VERSION = 1.0

class Collector(object):
    def __init__(self, host, port = 1180, version = DEFAULT_VERSION):
        self.host = host
        self.port = port
        self.version = version
        self.root_url = "http://%s:%s/%s/" % (self.host, self.port, self.version)

    def send(self, ce):
        url = self.root_url + "event/put"

        r = requests.post(url, data=to_jsons(ce))
        return r.status_code == 200


class Evaluator(object):
    def __init__(self, host, port = 1181, version = DEFAULT_VERSION):
        self.host = host
        self.port = port
        self.version = version
        self.root_url = "http://%s:%s/%s/" % (self.host, self.port, self.version)

    def event(self, expression, start = None, stop = None, limit = 100):
        url = self.root_url + "event"
        # pay attention : event query type does not need step
        return self._get(url, expression, start, stop, None, limit)

    def metric(self, expression, start = None, stop = None, step = "6e4", limit = 100):
        url = self.root_url + "metric"
        return self._get(url, expression, start, stop, step, limit)

    def _get(self, url, expression, start, stop, step, limit):
        params = {}

        if expression:
            params['expression'] = expression
        if start:
            params['start'] = start
        if stop:
            params['stop'] = stop
        if limit:
            params['limit'] = str(limit)
        if step:
            params['step'] = step

        r = requests.get(url, params=params)
        return r.status_code == 200 and json.loads(r.text) or None
