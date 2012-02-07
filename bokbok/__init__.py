import os
import flaskext.redis
from flask import Flask, g

app = Flask(__name__)
app.config.from_pyfile(os.environ.get('BOKBOK_SETTINGS',
                                      os.path.join(os.path.dirname(__file__),
                                                   '..', 'settings.py')))
app.debug = os.environ.get('FLASK_DEBUG', app.config.get('DEBUG'))
carbon_shards = app.config.get('CARBON_SHARDS', ['localhost'])
graphite_host = app.config.get('GRAPHITE_HOST', 'localhost')
graphite_options = app.config.get('GRAPHITE_OPTIONS', {})
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID',
                                   app.config.get('AWS_ACCESS_KEY_ID',
                                                  None))
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY',
                                   app.config.get('AWS_SECRET_ACCESS_KEY',
                                                  None))

from bokbok.views.frontend import frontend
app.register_blueprint(frontend)

@app.before_request
def before_request():
    from flask import g
    g.redis = flaskext.redis.init_redis(app)
