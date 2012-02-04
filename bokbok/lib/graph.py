import requests
from base64 import b64decode, b64encode
from flask import g
from json import dumps, loads
from uuid import uuid4
from time import time

class Graph(object):

    def __init__(self):
        self._redis_key = 'bokbok:graphs:blob'

    def load(self, _id):
        try:
            blob = loads(g.redis.hget(self._redis_key, _id))
        except TypeError:
            return None

        return b64decode(blob['image'])

    def save(self, url):
        _id = uuid4().hex
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            payload = dumps(dict(id=_id, created_at=time(), image=b64encode(r.content)))
            if g.redis.hset('bokbok:graphs:blob', _id, payload):
                return _id
            else:
                return None
        else:
            return None
