import json
from flask import Module, g, jsonify, render_template, request
from werkzeug.contrib.cache import SimpleCache

from bokbok import graphite_host, graphite_options
from bokbok.lib.metrics_search import MetricsSearch

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
    query = request.args.get('query')
    search = MetricsSearch()
    metrics = cache.get('bokbok:metrics_list')
    index = cache.get('bokbok:metrics_index')

    if not metrics:
        metrics = list(g.redis.smembers('metrics'))
        cache.set('bokbok:metrics_list', metrics, CACHE_TIMEOUT)
    if not index:
        index = search.index(metrics)
        cache.set('bokbok:metrics_index', index, CACHE_TIMEOUT)

    return jsonify(message=sorted(search.search(query, index)))