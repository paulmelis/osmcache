#!/usr/bin/env python3
import sys
from gevent.pywsgi import WSGIServer
from caching_server import app

port = 8888
if len(sys.argv) > 1:
    port = int(sys.argv[1])

print('Serving tiles on port %d' % port)
http_server = WSGIServer(('', port), app)
http_server.serve_forever()
