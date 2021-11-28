#!/usr/bin/env python3
import os, threading
from queue import Queue
from flask import Flask, send_file
import requests

TILE_DIR = 'tiles'

next_tile_server = 0
def get_osm_tile_server():
    global next_tile_server
    ts = ['a','b','c'][next_tile_server]
    next_tile_server = (next_tile_server+1) % 3
    return 'http://%s.tile.openstreetmap.org' % ts

class TileFetchThread(threading.Thread):
    
    """
    Responsible for fetching a tile image and saving it to disk"""
 
    def __init__(self, job_queue, result_queue):
        threading.Thread.__init__(self)
        self.job_queue = job_queue
        self.result_queue = result_queue
         
    def run(self):
        
        while True:
            
            tile_data = self.job_queue.get()
            if tile_data is None:
                # Time to quit
                break
                
            zoom, x, y, tilefile = tile_data
            url = '%s/%d/%d/%d.png' % (get_osm_tile_server(), zoom, x, y)
                
            # Make request to OSM
            #print('Fetching %s' % url)
            r = requests.get(url)
            
            if r.status_code == 200:
                # Save to disk
                with open(tilefile, 'wb') as f:
                    f.write(r.content)
        
            self.result_queue.put(('result', (zoom, x, y), r.status_code, tilefile))
        
        
class Manager(threading.Thread):
    
    NUM_THREADS = 2

    def __init__(self):
        threading.Thread.__init__(self)
        
        self.incoming_requests = Queue()    # Both tile requests, as well as fetch results
        self.job_queue = Queue()            # Jobs for fetch threads
        
        self.blocked_requests = {}
        
        self.fetch_threads = []
        for i in range(self.NUM_THREADS):
            th = TileFetchThread(self.job_queue, self.incoming_requests)
            th.start()
            self.fetch_threads.append(th)
        
    def run(self):
        
        while True:
            request = self.incoming_requests.get()
            
            if request[0] == 'tile':
                
                # Tile request
                zoom, x, y = request[1]
                result_queue = request[2]
            
                tilefile = os.path.join(TILE_DIR, str(zoom), str(x), str(y)+'.png')
                if os.path.isfile(tilefile):
                    # Tile available, can return result immediately
                    print('%s in cache' % tilefile)
                    result_queue.put((200, tilefile))
                else:
                    # Need to let thread fetch it
                    print('%s NOT in cache, fetching' % tilefile)
            
                    # Create parent dirs to tile file
                    dir = os.path.join(TILE_DIR, str(zoom), str(x))
                    if not os.path.isdir(dir):
                        os.makedirs(dir)
                        
                    key = (zoom, x, y)
                    if key not in self.blocked_requests:
                        self.blocked_requests[key] = [ result_queue ]
                    else:
                        self.blocked_requests[key].append(result_queue)
                    
                    # Add new job
                    self.job_queue.put((zoom, x, y, tilefile))
                
            else:
                assert request[0] == 'result'
                
                zoom, x, y = request[1]
                status_code = request[2]
                tilefile = request[3]
                
                print('z%d x%d y%d (%s) was fetched (%d)' % (zoom, x, y, tilefile, status_code))
                
                if status_code == 200:
                    result = (200, tilefile)
                else:
                    result = (status_code, None)
                
                key = zoom, x, y
                
                if key in self.blocked_requests:
                    for rqueue in self.blocked_requests[key]:
                        rqueue.put(result)
                    
                    del self.blocked_requests[key]
            
        # Signal fetch threads to quit 
        for i in range(self.NUM_THREADS):
            self.job_queue.put(None)

manager = Manager()
manager.daemon = True
manager.start()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/tile/<int:zoom>/<int:x>/<int:y>")
def tile(zoom, x, y):
    
    result_queue = Queue()
    manager.incoming_requests.put(('tile', (zoom, x, y), result_queue))

    # Blocks until file available
    status_code, tile_file = result_queue.get()
    
    if status_code == 200:
        return send_file(tile_file, mimetype='image/png', as_attachment=False)
    else:
        return 'Doh!', status_code
