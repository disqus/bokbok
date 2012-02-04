from flask import Module, Response, abort, g, jsonify, render_template, request

from bokbok import graphite_host, graphite_options
from bokbok.lib.graph import Graph
from bokbok.lib.metrics import Metrics

frontend = Module(__name__)

@frontend.route('/')
def index():
    return render_template('index.html',
                           graphite_host=graphite_host,
                           graphite_options=graphite_options)

@frontend.route('/graph/view/<_id>')
def load(_id):
    graph = Graph()
    image = graph.load(_id)

    if image:
        return Response(image, mimetype='image/png')
    else:
        abort(500)

@frontend.route('/graph/save', methods=['POST'])
def save():
    url = request.form.get('url', None)
    if not url:
        abort(400)

    graph = Graph()
    _id = graph.save(url)
    if not _id:
        abort(500)
    return jsonify(message=_id)

@frontend.route('/metrics.json')
def metrics():
    query = request.args.get('query', None)
    if not query:
        abort(400)

    metrics = Metrics()
    return jsonify(message=metrics.find(query, index)[:15])
