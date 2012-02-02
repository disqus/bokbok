from werkzeug.contrib.cache import SimpleCache

from bokbok import graphite_host

cache = SimpleCache()
CACHE_TIMEOUT = 86400

class Metrics(object):

    def cache(self):
        import json
        import requests
        from redis import Redis

        redis = Redis()
        r = requests.get('http://%s/metrics/index.json' % graphite_host)
        for line in json.loads(r.text):
            redis.sadd('bokbok:metrics_cache', line.lstrip('.'))

    def index(self, data):
        index = dict()
        for line in data:
            index[line] = None
        return index

    def find(self, query, index):
        from flask import g

        index = cache.get('bokbok:metrics_index')

        if not cache.get('bokbok:metrics_list'):
            metrics_list = list(g.redis.smembers('bokbok:metrics_cache'))
            cache.set('bokbok:metrics_list', metrics_list, CACHE_TIMEOUT)
        if not index:
            index = self.index(metrics_list)
            cache.set('bokbok:metrics_index', index, CACHE_TIMEOUT)

        return [metric for metric in sorted(index) if query in metric]
