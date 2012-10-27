__license__ = """
Copyright 2012 DISQUS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import requests
from base64 import b64decode, b64encode
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from flask import g
from json import dumps, loads
from time import time
from uuid import uuid4

from bokbok import aws_access_key_id, aws_bucket_name, aws_secret_access_key, graphite_host

class Graph(object):

    def __init__(self):
        self._blob_redis_key = 'bokbok:graphs:blob'
        self._config_redis_key = 'bokbok:graphs:config'
        self._blob = None
        self._config = None
        self._id = None

        self._s3_conn = S3Connection(aws_access_key_id,
                                     aws_secret_access_key)
        self.s3_bucket = self._s3_conn.create_bucket(aws_bucket_name)

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
                k = Key(self.s3_bucket)
                k.key = self.id
                self._blob_metadata = loads(g.redis.hget(self._blob_redis_key, self.id))
                if not self._blob_metadata:
                    raise AttributeError

                self._blob = b64decode(k.get_contents_as_string())
            return self._blob
        except TypeError:
            raise AttributeError

    @blob.setter
    def blob(self, data):
        self.id = uuid4().hex
        try:
            self._blob_metadata = dumps(dict(s3id=self.id, created_at=time()))
            self._blob = b64encode(data)
            k = Key(self.s3_bucket)
            k.key = self.id
            k.set_contents_from_string(self._blob)
            g.redis.hset(self._blob_redis_key, self.id, self._blob_metadata)
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

    def graph(self):
        if self.config:
            url = 'http://%s/render?%s' % (graphite_host,
                   '&'.join(['target=%s' % t for t in self.config['targets']]))

            r = requests.get(url, params=self.config['options'])
            if r.status_code == requests.codes.ok:
                return r.content
            else:
                return None
        else:
            return None
