import sys
sys.path.append('/usr/local/bokbok/releases/current')

activate_this = '/usr/local/bokbok/releases/current/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from bokbok import app as application
