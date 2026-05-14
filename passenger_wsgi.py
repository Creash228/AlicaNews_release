import sys, os

sys.path.append('/home/m/maksiy1x/maksiy1x.beget.tech/newproj')

sys.path.append('/home/m/maksiy1x/maksiy1x.beget.tech/venv/lib/python3.10/site-packages')

from newproj import app as application

from werkzeug.debug import DebuggedApplication
application.wsgi_app = DebuggedApplication(application.wsgi_app, True)
application.debug = True