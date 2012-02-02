import json
from flask import Module, g, jsonify, render_template, request
from werkzeug.contrib.cache import SimpleCache

from bokbok import graphite_host, graphite_options
from bokbok.lib.metrics import Metrics

frontend = Module(__name__)
cache = SimpleCache()
CACHE_TIMEOUT = 86400

@frontend.route('/')
def index():
    return render_template('index.html',
                           graphite_host=graphite_host,
                           graphite_options=graphite_options)

@frontend.route('/metrics.json')
def metrics():
    query = request.args.get('query', '')
    metrics = Metrics()
    index = cache.get('bokbok:metrics_index')

    if not cache.get('bokbok:metrics_list'):
        metrics_list = list(g.redis.smembers('metrics'))
        cache.set('bokbok:metrics_list', metrics_list, CACHE_TIMEOUT)
    if not index:
        index = metrics.index(metrics_list)
        cache.set('bokbok:metrics_index', index, CACHE_TIMEOUT)

    return jsonify(message=metrics.find(query, index)[:15])
