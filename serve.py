#!/usr/bin/env python3
from gevent.wsgi import WSGIServer
from caching_server import app

http_server = WSGIServer(('', 12347), app)
http_server.serve_forever()