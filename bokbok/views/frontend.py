from flask import Module, Response, abort, g, jsonify, render_template, request
from json import dumps

from bokbok import graphite_host, graphite_options
from bokbok.lib.graph import Graph
from bokbok.lib.metrics import Metrics

frontend = Module(__name__)

@frontend.route('/')
def index():
    graph_config = dict(options=graphite_options, targets=[])
    return render_template('index.html',
                           graphite_host=graphite_host,
                           graph=dumps(graph_config))

@frontend.route('/graph', methods=['POST'])
def save_config():
    config = request.form.get('config', None)
    if not config:
        abort(400)

    graph = Graph()

    try:
        graph.config = config
    except AttributeError:
        abort(500)

    if not graph.id:
        abort(500)

    return jsonify(message=graph.id)

@frontend.route('/graph/<pth>')
def load_config(pth):
    if '.' in pth:
        (_id, ext) = pth.split('.')
    else:
        _id = pth
        ext = None

    graph = Graph()
    graph.id = _id

    try:
        config = graph.config
    except AttributeError:
        abort(500)

    if ext == 'png':
        image = graph.graph()
        if image:
            return Response(image, mimetype='image/png')
        else:
            abort(404)

    return render_template('index.html',
                           graphite_host=graphite_host,
                           graph=dumps(config))

@frontend.route('/graph/snapshot', methods=['POST'])
def save_snapshot():
    url = request.form.get('url', None)
    if not url:
        abort(400)

    graph = Graph()
    _id = graph.snapshot(url)
    if not _id:
        abort(500)
    return jsonify(message=_id)

@frontend.route('/graph/snapshot/<_id>')
def load_blob(_id):
    graph = Graph()
    graph.id = _id
    image = graph.blob

    if image:
        return Response(image, mimetype='image/png')
    else:
        abort(500)

@frontend.route('/metrics.json')
def metrics():
    query = request.args.get('query', None)
    if not query:
        abort(400)

    metrics = Metrics()
    return jsonify(message=metrics.find(query, index)[:15])
