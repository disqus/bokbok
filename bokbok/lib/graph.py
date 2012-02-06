import requests
from base64 import b64decode, b64encode
from flask import g
from json import dumps, loads
from time import time
from uuid import uuid4

class Graph(object):

    def __init__(self):
        self._blob_redis_key = 'bokbok:graphs:blob'
        self._config_redis_key = 'bokbok:graphs:config'

        self._blob = None
        self._config = None
        self._id = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newid):
        self._id = newid

    @property
    def config(self):
        if not self.id:
            raise AttributeError

        try:
            if not self._config:
                self._config = loads(g.redis.hget(self._config_redis_key,
                                                  self.id))
        except TypeError:
            raise AttributeError

        return self._config

    @config.setter
    def config(self, config):
        if not self._id:
            self.id = uuid4().hex

        try:
            self._config = config
            g.redis.hset(self._config_redis_key, self.id, self._config)
        except:
            raise AttributeError

    @property
    def blob(self):
        if not self.id:
            raise AttributeError

        try:
            if not self._blob:
                self._blob = b64decode(loads(g.redis.hget(self._blob_redis_key,
                                                          self.id))['image'])
            return self._blob
        except TypeError:
            raise AttributeError

    @blob.setter
    def blob(self, data):
        self.id = uuid4().hex
        try:
            self._blob = dumps(dict(id=self.id, creatd_at=time(),
                                    image=b64encode(data)))
            g.redis.hset(self._blob_redis_key, self.id, self._blob)
        except TypeError:
            raise AttributeError

    def snapshot(self, url):
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            try:
                self.blob = r.content
                return self.id
            except AttributeError:
                return None
        else:
            return None
