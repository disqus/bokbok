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


class Metrics(object):

    def cache(self):
        import json
        import requests
        from redis import Redis

        from bokbok import carbon_shards

        redis = Redis()

        for shard in carbon_shards:
            r = requests.get('http://%s/metrics/index.json' % shard)
            _metrics = json.loads(r.text)
            for line in _metrics:
                redis.sadd('bokbok:metrics_cache', line.lstrip('.'))

    def index(self, data):
        index = dict()
        for line in data:
            index[line] = None
        return index

    def find(self, query, index):
        from flask import g
        from werkzeug.contrib.cache import SimpleCache

        cache = SimpleCache()
        CACHE_TIMEOUT = 86400
        index = cache.get('bokbok:metrics_index')

        if not cache.get('bokbok:metrics_list'):
            metrics_list = list(g.redis.smembers('bokbok:metrics_cache'))
            cache.set('bokbok:metrics_list', metrics_list, CACHE_TIMEOUT)
        if not index:
            index = self.index(metrics_list)
            cache.set('bokbok:metrics_index', index, CACHE_TIMEOUT)

        return [metric for metric in sorted(index) if query in metric]
