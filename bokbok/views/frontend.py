import json
from flask import Module, g, jsonify, render_template, request


from bokbok import graphite_host, graphite_options
from bokbok.lib.metrics import Metrics

frontend = Module(__name__)

@frontend.route('/')
def index():
    return render_template('index.html',
                           graphite_host=graphite_host,
                           graphite_options=graphite_options)

@frontend.route('/metrics.json')
def metrics():
    query = request.args.get('query', '')
    metrics = Metrics()

    return jsonify(message=metrics.find(query, index)[:15])
