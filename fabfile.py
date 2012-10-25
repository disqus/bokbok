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

from fabric.api import *
import time

env.name = 'bokbok'
env.time = int(time.time())

env.buildroot = '/tmp/%s/%d' % (env.name, env.time)
env.app = '%s/%s' % (env.buildroot, env.name)
env.deploy = '/usr/local/%s/releases' % env.name
env.hosts = ['CHANGEME']
env.repo = 'CHANGEME'
env.blob = '%s-%d.tgz' % (env.name, env.time)

def all():
  mkvirtualenv()
  prepare()
  build()
  deploy()
  restart_apache()

def deploy():
  put('/tmp/%s' % env.blob, '/tmp')
  with settings(hide('stdout')):
    with cd(env.deploy):
      run('mkdir %s' % env.time)
      with cd('%s' % env.time):
        run('tar xzf /tmp/%s' % env.blob)
      run('rm -f current; ln -sf %s current' % env.time)

def build():
  with settings(hide('stdout')):
    with lcd(env.buildroot):
      with prefix('. bin/activate'):
        local('pip install -r %s/requirements.txt' % env.buildroot)

      local('tar czf /tmp/%s .' % env.blob)

def mkvirtualenv():
  with settings(hide('stdout')):
    local('virtualenv --no-site-packages --setuptools --python python2.6 %s' % env.buildroot)

def prepare():
  dirs = ['tmp', env.name]

  with lcd(env.buildroot):
    local('mkdir %s' % ' '.join(dirs))
    with settings(hide('stdout')):
      with lcd('tmp'):
        with settings(hide('stderr')):
          local('git clone %s %s' % (env.repo, env.name))
        with lcd(env.name):
          local('git archive master | tar -xC %s' % env.buildroot)
        local('rm -rf %s' % env.name)

def restart_apache():
  run('sudo service apache2 restart')
