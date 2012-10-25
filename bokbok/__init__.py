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
